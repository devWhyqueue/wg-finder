import logging
from pathlib import Path

import requests

from wgfinder.app_config import get_required_config
from wgfinder.models import FlatAd

log = logging.getLogger(__name__)


def notify_by_telegram(flat_ad: FlatAd) -> None:
    """Send the rendered listing message and generated reply to Telegram."""
    content = _build_message(flat_ad)
    _send_telegram_message(content)
    _send_telegram_message(flat_ad.response)
    log.info(f"Message for {flat_ad} successfully sent!")


def _send_telegram_message(text: str) -> None:
    bot_token = get_required_config("telegram", "bot_token")
    chat_id = get_required_config("telegram", "chat_id")
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=30,
    )
    response.raise_for_status()


def _build_message(flat_ad: FlatAd) -> str:
    template = (
        Path(__file__).resolve().parent.parent / "templates" / "message.txt"
    ).read_text(encoding="UTF-8")
    message = (
        template.replace("{ROOMMATES}", str(flat_ad.roommates))
        .replace("{RENT}", str(flat_ad.rent))
        .replace("{SIZE}", str(flat_ad.size))
        .replace("{DISTRICT}", flat_ad.district)
        .replace("{DESC_SUMMARY}", flat_ad.desc_summary)
        .replace("{FREE_FROM}", flat_ad.free_from.strftime("%d.%m.%Y"))
        .replace("{URL}", flat_ad.url)
    )
    return message
