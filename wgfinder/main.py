import logging.config
from pathlib import Path
from time import sleep

import pkg_resources
import requests
from click import command, option

logging_config = pkg_resources.resource_filename(__name__, str(Path('config/logging.ini')))
logging.config.fileConfig(logging_config, disable_existing_loggers=False)
log = logging.getLogger("wgfinder.main")


@command()
@option('--mail', required=True)
def cli(mail):
    from wgfinder import scraper, messenger
    log.info("Starting to look for flat ads...")
    i = -1
    while True:
        try:
            flat_ads = scraper.find_shared_flats()
            for ad in flat_ads:
                messenger.notify_by_mail(ad, mail)
        except requests.exceptions.ConnectionError:
            log.error(f"Could not connect to server!")
        except AttributeError:
            log.error(f"Could not render page!")
        finally:
            i = _hourly_log(len(scraper.scraped_flat_ads), i)
            sleep(60)


def _hourly_log(flat_ads: int, i: int) -> int:
    i = i + 1
    if i == 60:
        log.info(f"Sill looking for flat ads, found {flat_ads} so far...")
        i = -1
    return i


if __name__ == '__main__':
    cli()
