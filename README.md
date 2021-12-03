# WG Finder

Defy the odds and find a home in Berlin!

# Usage

Execute main.py as a background process and log to file:

```
nohup python3 wgfinder/main.py --mail {MAIL} >> wgfinder-info.log 2>> wgfinder-error.log &
```
But do not forget to set the `SENDGRID_API_KEY` first!

To stop:

```
pkill -f wgfinder
```
