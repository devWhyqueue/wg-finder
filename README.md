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

Before starting the app, edit [`wgfinder/config/app.ini`](/mnt/d/Git/wg-finder/wgfinder/config/app.ini) and replace all `MUST_CHANGE` values:

```ini
[webshare]
proxy_url = MUST_CHANGE

[openai]
api_key = MUST_CHANGE

[telegram]
bot_token = MUST_CHANGE
chat_id = MUST_CHANGE
```

Create a Telegram bot with BotFather, copy the bot token into `bot_token`, start a chat with that bot, and set `chat_id` to the target chat you want to receive notifications in.

Execute main.py as a background process and log to file:

```
nohup uv run wgfinder >> wgfinder-info.log 2>> wgfinder-error.log &
```

To stop:

```
pkill -f wgfinder
```
