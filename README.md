<h1 align="center">TOKEN ONLINER</h1>

<p align="center">
  A lightweight multi-threaded Python script that keeps Discord accounts showing as online
  with a custom (or randomized) activity status.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. Automating user accounts
("self-botting") violates the [Discord Terms of Service](https://discord.com/terms)
and may lead to account suspension or termination. Only use tokens for accounts
that **you own**. The author is not responsible for any misuse or damage.

---

## ✨ Features

- 🟢 Keep multiple accounts online at once (one thread per token)
- 🎮 Custom status text and activity type: Playing, Streaming, Watching, Listening
- 🌙 Presence options: Online, Do Not Disturb, Idle
- 🎲 Random mode: random activity, app name, and presence per account
- 📜 Live console output with colored logs
- ⚡ Simple setup, no config files needed beyond `tokens.txt`

---

## 📦 Requirements

- Python 3.8 or newer
- The following packages:

```
websocket-client
colorama
```

---

## 🚀 Installation

```bash
git clone https://github.com/Yashit919/Discord-Tkn-Onliner.git
cd Discord-Tkn-Onliner
pip install -r requirements.txt
```

`requirements.txt`:

```
websocket-client
colorama
```

---

## ⚙️ Configuration

### 1. Add your tokens

Create a `tokens.txt` file in the project folder, with **one token per line**:

```
token_one_here
token_two_here
token_three_here
```

### 2. Edit the settings

Open the script and change the values between the `Change here` and `Stop changing here` markers:

| Variable      | Description                                                            | Example            |
|---------------|------------------------------------------------------------------------|--------------------|
| `GAME`        | Text shown as the activity name                                        | `"Minecraft"`      |
| `type_`       | Activity type: `types[0]` Playing, `[1]` Streaming, `[2]` Watching, `[3]` Listening | `types[0]` |
| `status`      | Presence: `status[0]` Online, `[1]` Do Not Disturb, `[2]` Idle         | `status[0]`        |
| `random_`     | `True` = random activity/status per account, `False` = use your settings | `False`          |
| `stream_text` | Stream URL used when the type is Streaming                             | `"https://twitch.tv/yourname"` |

---

## ▶️ Usage

```bash
python main.py
```

You should see something like:

```
[i] Importing modules...
[i] 3 tokens found in tokens.txt
[i] Starting...
[+] Tokens are online
[i] <token> is online 1/3
```

Press `Ctrl + C` to stop.

---

## 📁 Project Structure

```
.
├── main.py            # the onliner script
├── tokens.txt         # your tokens (one per line), never commit this!
├── requirements.txt
└── README.md
```

> 🔒 Add `tokens.txt` to your `.gitignore` so you never upload tokens by accident.

---

## 🛠️ Troubleshooting

| Problem                          | Fix                                                       |
|----------------------------------|-----------------------------------------------------------|
| `No tokens found in tokens.txt`  | Make sure the file exists and has at least one token      |
| Token shows offline              | The token may be invalid, expired, or the account locked  |
| `ModuleNotFoundError`            | Run `pip install -r requirements.txt`                     |
| Connection errors                | Check your internet connection or try fewer tokens at once |

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

---

<p align="center">Made by <a href="https://github.com/Yashit919">Yashit919</a></p>
