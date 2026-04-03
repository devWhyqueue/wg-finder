import logging
import re
from datetime import datetime
from pprint import pformat
from urllib.parse import urljoin

import backoff
from bs4 import BeautifulSoup

from wgfinder.app_config import get_required_config
from wgfinder.models import FlatAd
from wgfinder.util import requests_get

log = logging.getLogger(__name__)
PUBLISHER_BLACKLIST = ["Housing", "Spacest"]

scraped_flat_ads = []


class PageRenderError(Exception):
    pass


def _get_search_url() -> str:
    base_url = get_required_config(
        "wg_gesucht", "base_url", allow_placeholder=True
    ).rstrip("/")
    search_query = get_required_config(
        "wg_gesucht", "search_query", allow_placeholder=True
    ).lstrip("/")
    return f"{base_url}/{search_query}"


def find_shared_flats() -> list[FlatAd]:
    """Fetch and parse currently available flat ads from WG-Gesucht."""
    html = requests_get(_get_search_url()).text
    flat_ads = _parse_flat_ads(html)
    scraped_flat_ads.extend(flat_ads)
    (
        log.info(
            f"Found {len(flat_ads)} new flat ad{'s' if len(flat_ads) > 1 else ''}."
        )
        if len(flat_ads)
        else None
    )
    log.debug(pformat(flat_ads))
    return flat_ads


def _parse_flat_ads(html: str) -> list[FlatAd]:
    page = BeautifulSoup(html, features="html.parser")
    flat_ads = []
    base_url = get_required_config(
        "wg_gesucht", "base_url", allow_placeholder=True
    ).rstrip("/")
    for div in page.select("#main_content .wgg_card.offer_list_item"):
        parent_div = div.div
        if parent_div is None:
            continue
        printonly_div = parent_div.select_one("div .printonly")
        if printonly_div is None or printonly_div.a is None:
            continue
        href = printonly_div.a.get("href")
        if not isinstance(href, str):
            continue
        url = urljoin(f"{base_url}/", href)
        publisher = div.select_one("span.ml5")
        if publisher is None:
            continue
        publisher_text = publisher.get_text(strip=True)
        online_since = div.select_one("span[style*='color: #218700;']")
        online_since = online_since.text if online_since else ""
        uploaded_recently = any(word in online_since for word in ["Sekunde", "Minute"])
        # Ignore ads
        if (
            "asset_id" not in url
            and not any(word in publisher_text for word in PUBLISHER_BLACKLIST)
            and uploaded_recently
        ):
            info_divs = printonly_div.find_all("div")
            if len(info_divs) < 3:
                continue
            rent_size = info_divs[0].find_all("b")
            if len(rent_size) < 2:
                continue
            info_text = info_divs[1].get_text(" ", strip=True)
            roommates = int(info_text[0])
            free_from = datetime.strptime(
                info_divs[2].text.strip(), "Verfügbar: %d.%m.%Y"
            ).date()
            rent = int(rent_size[0].text.split(" ")[0])
            size = int(rent_size[1].text.strip()[:-2])
            district = _extract_district(info_text)
            description = _get_flat_description(url)
            if (
                description is not None
                and uploaded_recently
                and rent > 100
                and size < 40
                and len(description) > 500
            ):
                flat_ads.append(
                    FlatAd(
                        url,
                        roommates,
                        rent,
                        size,
                        district,
                        free_from,
                        description,
                        publisher_text,
                    )
                )
    return [ad for ad in flat_ads if ad not in scraped_flat_ads]


@backoff.on_exception(backoff.expo, PageRenderError, max_tries=5)
def _get_flat_description(url: str) -> str | None:
    details_html = requests_get(url).text
    details_page = BeautifulSoup(details_html, features="html.parser")

    # Check if ad is deactivated
    deactivated_element = details_page.select_one(
        "div.alert.alert-without-icon-alt.border-orange"
    )
    if deactivated_element:
        log.warning(f"Ad is deactivated and will be skipped: {url}")
        return None

    headline = details_page.select(".detailed-view-title span[class]")
    if not headline or len(headline) < 2:
        raise PageRenderError(f"Could not render detail page: {url}")
    headline_text = headline[1].text.strip()
    description_divs = details_page.select("div[id^='freitext']")
    description = "\n".join([div.text.strip() for div in description_divs])
    return f"{headline_text}\n{description}"


def _extract_district(info_text: str) -> str:
    """Extract district from normalized info text like '2er WG | Berlin Prenzlauer Berg |'"""
    match = re.search(r"\|\s*Berlin\s+([^|]+?)\s*(?:\||$)", info_text)
    if match:
        return match.group(1).strip()

    parts = info_text.split("|")
    if len(parts) > 1:
        segment = parts[1].split("|")[0].strip()
        if segment.startswith("Berlin"):
            remainder = segment[len("Berlin") :].strip()
            return remainder
        return segment
    return ""
