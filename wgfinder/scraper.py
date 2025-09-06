import logging
from datetime import datetime
from pprint import pformat

import backoff
from bs4 import BeautifulSoup
import re

from wgfinder.models import FlatAd
from wgfinder.util import requests_get

log = logging.getLogger(__name__)
WG_GESUCHT_BASE_URL = "https://www.wg-gesucht.de"
WG_GESUCHT_SEARCH_QUERY = (
    "wg-zimmer-in-Berlin.8.0.1.0.html?offer_filter=1&city_id=8&noDeact=1&dFr=1748772000"
    "&dTo=1761994800&sMin=15&rMax=760&wgSea=2&wgMnF=1&wgMxT=3&wgAge=27&img_only=1&exContAds=1"
    "&wgArt=12,1,11,19,16,15,7,5,13,22&ot=126,85077,132,85079,85080,151,163,85086,165,171,178"
    ",85094,184,189&categories[]=0&rent_types[]=2&user_filter_id=9808663"
)
PUBLISHER_BLACKLIST = ["Housing", "Spacest"]

scraped_flat_ads = []


class PageRenderError(Exception):
    pass


def find_shared_flats() -> list[FlatAd]:
    """Fetch and parse currently available flat ads from WG-Gesucht."""
    html = requests_get(f"{WG_GESUCHT_BASE_URL}/{WG_GESUCHT_SEARCH_QUERY}").text
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
    for div in page.select("#main_content .wgg_card.offer_list_item"):
        printonly_div = div.div.select_one("div .printonly")
        url = f'{WG_GESUCHT_BASE_URL}{printonly_div.a["href"]}'
        publisher = div.select_one("span.ml5")
        online_since = div.select_one("span[style*='color: #218700;']")
        online_since = online_since.text if online_since else ""
        uploaded_recently = any(word in online_since for word in ["Sekunde", "Minute"])
        # Ignore ads
        if "asset_id" not in url and not any(word in publisher.text for word in PUBLISHER_BLACKLIST) and uploaded_recently:
            info_divs = printonly_div.find_all("div")
            info_text = info_divs[1].get_text(" ", strip=True)
            roommates = int(info_text[0])
            free_from = datetime.strptime(
                info_divs[2].text.strip(), "Verfügbar: %d.%m.%Y"
            ).date()
            rent = int(info_divs[0].find_all("b")[0].text.split(" ")[0])
            size = int(info_divs[0].find_all("b")[1].text.strip()[:-2])
            district = _extract_district(info_text)
            description = _get_flat_description(url)
            if description is not None and uploaded_recently and rent > 100 and size < 40 and len(description) > 500:
                flat_ads.append(
                    FlatAd(url, roommates, rent, size, district, free_from, description, publisher)
                )
    return [ad for ad in flat_ads if ad not in scraped_flat_ads]


@backoff.on_exception(backoff.expo, PageRenderError, max_tries=5)
def _get_flat_description(url: str) -> str | None:
    details_html = requests_get(url).text
    details_page = BeautifulSoup(details_html, features="html.parser")
    
    # Check if ad is deactivated
    deactivated_element = details_page.select_one("div.alert.alert-without-icon-alt.border-orange")
    if deactivated_element:
        log.warning(f"Ad is deactivated and will be skipped: {url}")
        return None
    
    headline = details_page.select('.detailed-view-title span[class]')
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
            remainder = segment[len("Berlin"):].strip()
            return remainder
        return segment
    return ""
