import logging.config
from pathlib import Path

import pkg_resources

from wgfinder.scraper import find_shared_flats

logging_config = pkg_resources.resource_filename(__name__, str(Path('config/logging.ini')))
logging.config.fileConfig(logging_config, disable_existing_loggers=False)

# @command()
# @argument('username')
# @argument('password')
# @option('--phone-number', required=True)
# @option('--chromium-path', type=click.Path())
# def cli(username, password, chromium_path, phone_number):
#     appointment = AppointmentFinder(Web(chromium_path))
#     appointment_pairs = appointment.find_all(username, password)
#     notifier = SMSNotifier(phone_number)
#     if appointment_pairs:
#         msg = build_message(appointment_pairs)
#         notifier.send_message(msg)
#

if __name__ == '__main__':
    # cli()
    find_shared_flats()
