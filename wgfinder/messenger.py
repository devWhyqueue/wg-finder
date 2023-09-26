import logging
from pathlib import Path

import pywhatkit as kit

from wgfinder.models import FlatAd

log = logging.getLogger(__name__)


def notify_by_whatsapp(flat_ad: FlatAd, recipient: str):
    content = _build_message(flat_ad)
    kit.sendwhatmsg_instantly(recipient, content, tab_close=True)
    log.info(f"Message for {flat_ad} successfully sent!")


def _build_message(flat_ad: FlatAd) -> str:
    template = (Path(__file__).parent / Path("templates/message.txt")).read_text(encoding="UTF-8")
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
