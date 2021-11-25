import logging
import os
from pathlib import Path

from sendgrid import Mail, SendGridAPIClient

from wgfinder.models import FlatAd

log = logging.getLogger(__name__)


def notify_by_mail(flat_ad: FlatAd, recipient: str):
    content = _build_message(flat_ad)
    mail = Mail(
        from_email='dev.yannik.queisler@gmail.com',
        to_emails=recipient,
        subject='Neue WG verfügbar!',
        html_content=content)
    sendgrid_client = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sendgrid_client.send(mail)
    log.debug(response.status_code)


def _build_message(flat_ad: FlatAd) -> str:
    template = Path("templates/mail_template.html").read_text(encoding="UTF-8")
    message = template \
        .replace("{ROOMMATES}", str(flat_ad.roommates)) \
        .replace("{RENT}", str(flat_ad.rent)) \
        .replace("{SIZE}", str(flat_ad.size)) \
        .replace("{DISTRICT}", flat_ad.district) \
        .replace("{URL}", flat_ad.url)
    return message
