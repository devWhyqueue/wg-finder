# WG Finder

Defy the odds and find a home in Berlin!

# Usage

Execute main.py as a background process and log to file:

```
export SENDGRID_API_KEY={SENDGRID_API_KEY}
nohup python3 wgfinder/main.py --mail {MAIL} >> wgfinder-info.log 2>> wgfinder-error.log &
```

To stop:

```
pkill -f wgfinder
```
