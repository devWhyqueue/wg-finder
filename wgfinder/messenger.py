import logging
import os
from pathlib import Path

from sendgrid import Mail, SendGridAPIClient, SendGridException

from wgfinder.models import FlatAd

log = logging.getLogger(__name__)


def notify_by_mail(flat_ad: FlatAd, recipient: str):
    try:
        content = _build_message(flat_ad)
        mail = Mail(
            from_email='dev.yannik.queisler@gmail.com',
            to_emails=recipient,
            subject=f'{flat_ad.size}m² {flat_ad.roommates}er WG in {flat_ad.district}',
            html_content=content)
        sendgrid_client = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        sendgrid_client.send(mail)
        log.info(f"Mail for {flat_ad} successfully sent!")
    except SendGridException:
        log.exception(f"Mail for {flat_ad} could not be sent!")
        log.debug(f"Mail for {flat_ad} could not be sent!", exc_info=True)


def _build_message(flat_ad: FlatAd) -> str:
    template = (Path(__file__).parent / Path("templates/mail.html")).read_text(encoding="UTF-8")
    message = template \
        .replace("{ROOMMATES}", str(flat_ad.roommates)) \
        .replace("{RENT}", str(flat_ad.rent)) \
        .replace("{SIZE}", str(flat_ad.size)) \
        .replace("{DISTRICT}", flat_ad.district) \
        .replace("{DESC_SUMMARY}", flat_ad.desc_summary) \
        .replace("{RESPONSE}", flat_ad.response) \
        .replace("{FREE_FROM}", flat_ad.free_from.strftime("%d.%m.%Y")) \
        .replace("{URL}", flat_ad.url)
    return message
