<h1 align="center">TOKEN ONLINER</h1>

<p align="center">
  A lightweight, async Python script that keeps your Discord accounts showing as online
  with a custom or randomized activity status.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/gateway-v10-5865F2?logo=discord&logoColor=white" alt="Discord Gateway v10">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. Automating user accounts
("self-botting") violates the [Discord Terms of Service](https://discord.com/terms)
and can lead to account suspension or termination. Only use tokens from accounts
that **you own**. The author is not responsible for any misuse or damage.

---

## ✨ Features

- 🟢 **Multi-account**: keeps any number of accounts online at the same time
- 🎮 **Custom activity**: Playing, Streaming, Watching, or Listening
- 🌙 **Presence control**: Online, Do Not Disturb, or Idle
- 🎲 **Random mode**: random activity, app name, and presence for each account
- 🔄 **Status rotation**: optionally re-roll the random status every N minutes
- 🔌 **Stable connections**: proper heartbeat, session resume, and auto-reconnect with backoff
- 🚫 **Smart token handling**: skips blank lines and duplicates, stops on invalid tokens
- 🔒 **Safe logs**: tokens are masked in the console output
- ⚡ **Async**: runs on `asyncio`, so there are no thread-per-token overheads

---

## 📦 Requirements

- Python **3.9** or newer
- Packages listed in `requirements.txt`:

```
websockets>=12.0
colorama>=0.4.6
```

---

## 🚀 Installation

```bash
git clone https://github.com/Yashit919/Discord-Tkn-Onliner.git
cd Discord-Tkn-Onliner
pip install -r requirements.txt
```

---

## 🔑 Setup: `tokens.txt`

The script reads accounts from a file called **`tokens.txt`** in the project folder.
Put **one token per line**, with no quotes and no extra characters:

```
your_first_token_here
your_second_token_here
your_third_token_here
```

Notes:

- Blank lines and duplicate tokens are ignored automatically.
- `tokens.txt` is listed in `.gitignore`, so it will **not** be uploaded when you push the repo.
- 🚨 **Never share or commit your tokens.** Anyone with a token has full access to that account.

---

## ⚙️ Configuration

Open `main.py` and edit the values in the **Settings** section near the top:

| Setting           | Description                                                         | Default                      |
|-------------------|---------------------------------------------------------------------|------------------------------|
| `TOKENS_FILE`     | Path to your tokens file                                            | `"tokens.txt"`               |
| `ACTIVITY_TEXT`   | Text shown as the activity name                                     | `"MY TEXT"`                  |
| `ACTIVITY_TYPE`   | `playing`, `streaming`, `watching`, or `listening`                  | `"playing"`                  |
| `STREAM_URL`      | Twitch or YouTube link, only used when type is `streaming`          | `"https://twitch.tv/yourname"` |
| `STATUS`          | `online`, `dnd`, or `idle`                                          | `"online"`                   |
| `RANDOM_MODE`     | `True` = random activity and status per account                     | `False`                      |
| `ROTATE_MINUTES`  | In random mode, re-roll every N minutes (`0` = never)               | `0`                          |
| `STAGGER_SECONDS` | Delay between account logins, which helps avoid rate limits         | `1.5`                        |

**Example: stream status on Do Not Disturb**

```python
ACTIVITY_TEXT = "Live now"
ACTIVITY_TYPE = "streaming"
STREAM_URL = "https://twitch.tv/yourname"
STATUS = "dnd"
```

**Example: random status that changes every 30 minutes**

```python
RANDOM_MODE = True
ROTATE_MINUTES = 30
```

---

## ▶️ Usage

```bash
python main.py
```

Example output:

```
[i] 3 token(s) loaded
[+] MTIzND...x9Zk (1/3) online as 'MY TEXT' / online
[+] MTIzND...a1Qp (2/3) online as 'MY TEXT' / online
[+] MTIzND...m7Lw (3/3) online as 'MY TEXT' / online
```

Press `Ctrl + C` to stop.

---

## 📁 Project Structure

```
.
├── main.py            # the onliner script
├── tokens.txt         # your tokens, one per line (not committed)
├── requirements.txt   # Python dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Troubleshooting

| Problem                              | Fix                                                                  |
|--------------------------------------|----------------------------------------------------------------------|
| `tokens.txt not found`               | Create `tokens.txt` in the same folder as `main.py`                  |
| `No tokens found`                    | Make sure the file has at least one token on its own line            |
| `stopped: invalid token`             | The token is wrong, expired, or the account was reset or disabled    |
| Account shows offline                | Check the token is valid and that the account isn't locked           |
| `ModuleNotFoundError`                | Run `pip install -r requirements.txt`                                |
| Repeated `disconnected` messages     | Check your internet connection, or try fewer accounts at once        |
| Streaming status doesn't show        | `STREAM_URL` must be a valid Twitch or YouTube link                  |

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

---

<p align="center">Made by <a href="https://github.com/Yashit919">@Yashit919</a></p>
