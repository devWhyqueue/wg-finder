# WG Finder

Defy the odds and find a home in Berlin!

# Prerequisites

- Venv: `python3 -m pip install --user virtualenv`
- Poetry: `python3 -m pip install poetry`

# Installation

Create and activate venv:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```
poetry install
```

# Usage

Before starting the app, edit [`wgfinder/config/app.ini`](/mnt/d/Git/wg-finder/wgfinder/config/app.ini) and replace all `MUST_CHANGE` values:

```ini
[webshare]
proxy_url = MUST_CHANGE

[openai]
api_key = MUST_CHANGE
```

Execute main.py as a background process and log to file:

```
nohup python3 wgfinder/main.py --phone {PHONE} >> wgfinder-info.log 2>> wgfinder-error.log &
```

To stop:

```
pkill -f wgfinder
```
