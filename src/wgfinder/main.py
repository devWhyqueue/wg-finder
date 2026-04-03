import logging.config
from importlib.resources import as_file, files
from time import sleep

import requests
from click import command

from wgfinder import chatgpt, messenger, scraper

with as_file(files("wgfinder").joinpath("config", "logging.ini")) as logging_config:
    logging.config.fileConfig(logging_config, disable_existing_loggers=False)
log = logging.getLogger("wgfinder.main")


@command()
def cli() -> None:
    """Continuously poll WG-Gesucht and send matching ads to Telegram."""
    log.info("Starting to look for flat ads...")
    i = -1
    while True:
        try:
            flat_ads = scraper.find_shared_flats()
            for ad in flat_ads:
                ad.desc_summary = chatgpt.summarize_flat_ad(ad)
                ad.response = chatgpt.generate_response(ad)
                messenger.notify_by_telegram(ad)
        except requests.exceptions.ConnectionError:
            log.error("Could not connect to server!")
            log.debug("Could not connect to server!", exc_info=True)
        except AttributeError:
            log.error("Could not render page!")
            log.debug("Could not render page!", exc_info=True)
        finally:
            i = _hourly_log(len(scraper.scraped_flat_ads), i)
            sleep(60)


def _hourly_log(flat_ads: int, i: int) -> int:
    i = i + 1
    if i == 60:
        log.info(f"Sill looking for flat ads, found {flat_ads} so far...")
        i = -1
    return i


if __name__ == "__main__":
    cli()
