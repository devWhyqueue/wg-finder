# WG Finder

Defy the odds and find a home in Berlin!

# Prerequisites

- `uv`

# Installation

Create the virtual environment and install dependencies:

```
uv sync --dev
```

# Usage

Before starting the app, set the secret values in [`.env`](/mnt/d/Git/wg-finder/.env) and keep the non-secret defaults in [`src/wgfinder/config/app.ini`](/mnt/d/Git/wg-finder/src/wgfinder/config/app.ini):

```dotenv
WEBSHARE_PROXY_URL=MUST_CHANGE
OPENAI_API_KEY=MUST_CHANGE
TELEGRAM_BOT_TOKEN=MUST_CHANGE
TELEGRAM_CHAT_ID=MUST_CHANGE
```

`app.ini` still controls non-secret settings such as the WG-Gesucht query and the OpenAI model names.

Create a Telegram bot with BotFather, copy the bot token into `TELEGRAM_BOT_TOKEN`, start a chat with that bot, and set `TELEGRAM_CHAT_ID` to the target chat you want to receive notifications in.

Execute main.py as a background process and log to file:

```
nohup uv run wgfinder >> wgfinder-info.log 2>> wgfinder-error.log &
```

To stop:

```
pkill -f wgfinder
```
