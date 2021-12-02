import logging.config
from pathlib import Path
from time import sleep

import pkg_resources
from click import command, option

from wgfinder.messenger import notify_by_mail
from wgfinder.scraper import find_shared_flats

logging_config = pkg_resources.resource_filename(__name__, str(Path('config/logging.ini')))
logging.config.fileConfig(logging_config, disable_existing_loggers=False)


@command()
@option('--mail', required=True)
def cli(mail):
    while True:
        flat_ads = find_shared_flats()
        for ad in flat_ads:
            notify_by_mail(ad, mail)
        sleep(60)


if __name__ == '__main__':
    cli()
