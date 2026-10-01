import asyncio
import json
import random
import sys
from pathlib import Path
 
import websockets
from colorama import Fore, Style, init
 
init(autoreset=True)
 
BANNER = r"""
████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗
╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
   ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
   ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
   ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
 
 ██████╗ ███╗   ██╗██╗     ██╗███╗   ██╗███████╗██████╗ 
██╔═══██╗████╗  ██║██║     ██║████╗  ██║██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║██║     ██║██╔██╗ ██║█████╗  ██████╔╝
██║   ██║██║╚██╗██║██║     ██║██║╚██╗██║██╔══╝  ██╔══██╗
╚██████╔╝██║ ╚████║███████╗██║██║ ╚████║███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
 
                    ─────  M A D E   B Y  ─────
 
██╗   ██╗ █████╗ ███████╗██╗  ██╗██╗████████╗ █████╗  ██╗ █████╗ 
╚██╗ ██╔╝██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔══██╗███║██╔══██╗
 ╚████╔╝ ███████║███████╗███████║██║   ██║   ╚██████║╚██║╚██████║
  ╚██╔╝  ██╔══██║╚════██║██╔══██║██║   ██║    ╚═══██║ ██║ ╚═══██║
   ██║   ██║  ██║███████║██║  ██║██║   ██║    █████╔╝ ██║ █████╔╝
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝    ╚════╝  ╚═╝ ╚════╝ 
"""
 
# ───────────────────────── Settings ─────────────────────────
TOKENS_FILE = "tokens.txt"
 
ACTIVITY_TEXT = "MY TEXT"        # activity name shown under the account
ACTIVITY_TYPE = "playing"         # playing | streaming | watching | listening
STREAM_URL = "https://twitch.tv/yourname"  # only used for "streaming"
STATUS = "online"                 # online | dnd | idle
 
RANDOM_MODE = False               # random activity/status per account
ROTATE_MINUTES = 0                # in random mode: re-roll every N minutes (0 = never)
STAGGER_SECONDS = 1.5             # delay between account logins
# ────────────────────────────────────────────────────────────
 
GATEWAY = "wss://gateway.discord.gg"
API_QUERY = "/?v=10&encoding=json"
 
TYPE_IDS = {"playing": 0, "streaming": 1, "listening": 2, "watching": 3}
STATUSES = ["online", "dnd", "idle"]
 
RANDOM_POOL = {
    "playing": ["Minecraft", "Roblox", "Badlion", "The Elder Scrolls Online", "DCS World"],
    "listening": ["Spotify", "Deezer", "Apple Music", "YouTube Music", "SoundCloud", "Tidal"],
    "watching": ["YouTube", "Twitch", "Netflix"],
}
 
# Close codes that mean "do not retry"
FATAL_CLOSE_CODES = {4004, 4010, 4011, 4012, 4013, 4014}
 
 
def mask(token: str) -> str:
    return f"{token[:6]}...{token[-4:]}" if len(token) > 12 else "***"
 
 
def log(color: str, tag: str, msg: str) -> None:
    print(f"{color}[{tag}]{Style.RESET_ALL} {msg}")
 
 
def load_tokens(path: str) -> list[str]:
    file = Path(path)
    if not file.exists():
        log(Fore.RED, "!", f"{path} not found. Create it with one token per line.")
        sys.exit(1)
    seen, tokens = set(), []
    for line in file.read_text(encoding="utf-8").splitlines():
        token = line.strip().strip('"')
        if token and token not in seen:
            seen.add(token)
            tokens.append(token)
    if not tokens:
        log(Fore.RED, "!", f"No tokens found in {path}")
        sys.exit(1)
    return tokens
 
 
def build_presence() -> dict:
    """Return a presence dict ready for the gateway."""
    if RANDOM_MODE:
        kind = random.choice(list(RANDOM_POOL) + ["streaming"])
        status = random.choice(STATUSES)
        name = ACTIVITY_TEXT if kind == "streaming" else random.choice(RANDOM_POOL[kind])
    else:
        kind, status, name = ACTIVITY_TYPE.lower(), STATUS, ACTIVITY_TEXT
 
    activity = {"name": name, "type": TYPE_IDS.get(kind, 0)}
    if kind == "streaming":
        activity["url"] = STREAM_URL
    return {"since": None, "activities": [activity], "status": status, "afk": False}
 
 
class Account:
    """One gateway connection with heartbeat, resume and reconnect handling."""
 
    def __init__(self, token: str, index: int, total: int):
        self.token = token
        self.label = f"{mask(token)} ({index}/{total})"
        self.seq = None
        self.session_id = None
        self.resume_url = None
        self.acked = True
        self.presence = build_presence()
 
    # ── gateway payloads ──
    async def identify(self, ws):
        await ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {"os": sys.platform, "browser": "Chrome", "device": ""},
                "presence": self.presence,
            },
        }))
 
    async def resume(self, ws):
        await ws.send(json.dumps({
            "op": 6,
            "d": {"token": self.token, "session_id": self.session_id, "seq": self.seq},
        }))
 
    async def heartbeat_loop(self, ws, interval: float):
        await asyncio.sleep(interval * random.random())  # jitter per Discord docs
        while True:
            if not self.acked:  # zombie connection, force reconnect
                await ws.close(code=4000, reason="missed heartbeat ack")
                return
            self.acked = False
            await ws.send(json.dumps({"op": 1, "d": self.seq}))
            await asyncio.sleep(interval)
 
    async def rotate_loop(self, ws):
        while True:
            await asyncio.sleep(ROTATE_MINUTES * 60)
            self.presence = build_presence()
            await ws.send(json.dumps({"op": 3, "d": self.presence}))
            name = self.presence["activities"][0]["name"]
            log(Fore.CYAN, "~", f"{self.label} rotated to '{name}' / {self.presence['status']}")
 
    # ── main loop ──
    async def run(self):
        backoff = 1
        while True:
            base = self.resume_url if self.session_id else GATEWAY
            tasks = []
            try:
                async with websockets.connect(base + API_QUERY, max_size=None) as ws:
                    hello = json.loads(await ws.recv())
                    interval = hello["d"]["heartbeat_interval"] / 1000
                    self.acked = True
                    tasks.append(asyncio.create_task(self.heartbeat_loop(ws, interval)))
 
                    if self.session_id:
                        await self.resume(ws)
                    else:
                        await self.identify(ws)
 
                    async for raw in ws:
                        msg = json.loads(raw)
                        op, data = msg["op"], msg.get("d")
                        if msg.get("s") is not None:
                            self.seq = msg["s"]
 
                        if op == 0 and msg["t"] == "READY":
                            self.session_id = data["session_id"]
                            self.resume_url = data["resume_gateway_url"]
                            backoff = 1
                            name = self.presence["activities"][0]["name"]
                            log(Fore.GREEN, "+", f"{self.label} online as '{name}' / {self.presence['status']}")
                            if RANDOM_MODE and ROTATE_MINUTES > 0:
                                tasks.append(asyncio.create_task(self.rotate_loop(ws)))
                        elif op == 0 and msg["t"] == "RESUMED":
                            backoff = 1
                            log(Fore.GREEN, "+", f"{self.label} session resumed")
                        elif op == 1:  # server asked for a heartbeat
                            await ws.send(json.dumps({"op": 1, "d": self.seq}))
                        elif op == 7:  # reconnect requested
                            await ws.close(code=4000)
                        elif op == 9:  # invalid session
                            if not data:
                                self.session_id = self.seq = None
                            await asyncio.sleep(random.uniform(1, 5))
                            await ws.close(code=4000)
                        elif op == 11:
                            self.acked = True
 
            except websockets.ConnectionClosed as exc:
                code = exc.rcvd.code if exc.rcvd else None
                if code in FATAL_CLOSE_CODES:
                    reason = "invalid token" if code == 4004 else f"close code {code}"
                    log(Fore.RED, "!", f"{self.label} stopped: {reason}")
                    return
                log(Fore.YELLOW, "i", f"{self.label} disconnected ({code}), retrying in {backoff}s")
            except (OSError, asyncio.TimeoutError, websockets.WebSocketException) as exc:
                log(Fore.YELLOW, "i", f"{self.label} error: {exc}, retrying in {backoff}s")
            finally:
                for task in tasks:
                    task.cancel()
 
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
 
 
async def main():
    print(BANNER)
 
    tokens = load_tokens(TOKENS_FILE)
    log(Fore.GREEN, "i", f"{len(tokens)} token(s) loaded")
    if ACTIVITY_TYPE.lower() == "streaming" and not RANDOM_MODE:
        log(Fore.YELLOW, "i", f"Streaming URL: {STREAM_URL}")
 
    accounts = [Account(t, i + 1, len(tokens)) for i, t in enumerate(tokens)]
    jobs = []
    for acc in accounts:
        jobs.append(asyncio.create_task(acc.run()))
        await asyncio.sleep(STAGGER_SECONDS)
 
    await asyncio.gather(*jobs)
 
 
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        log(Fore.YELLOW, "i", "Stopped by user")
 
