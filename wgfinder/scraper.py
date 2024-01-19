import logging
from datetime import datetime
from pprint import pformat

import backoff
from bs4 import BeautifulSoup

from wgfinder.models import FlatAd
from wgfinder.util import requests_get

log = logging.getLogger(__name__)
WG_GESUCHT_BASE_URL = "https://www.wg-gesucht.de"
WG_GESUCHT_SEARCH_QUERY = ("wg-zimmer-in-Berlin.8.0.1.0.html?user_filter_id=9808663&categories%5B0%5D=0&city_id=8&dFr"
                           "=1704110400&dTo=1714564800&exc=2&img=1&img_only=1&noDeact=1&rMax=700&radAdd=Bodestraße"
                           "&radDis=6000&radLat=52.518218320448&radLng=13.398499672848&rent_types%5B0%5D=2&sMin=15"
                           "&wgAge=25&wgArt=12%2C1%2C11%2C19%2C16%2C15%2C7%2C5%2C13%2C22&wgMnF=1&wgMxT=5&wgSea=2")

scraped_flat_ads = []


class PageRenderError(Exception):
    pass


def find_shared_flats() -> list[FlatAd]:
    html = requests_get(f"{WG_GESUCHT_BASE_URL}/{WG_GESUCHT_SEARCH_QUERY}").text
    flat_ads = _parse_flat_ads(html)
    scraped_flat_ads.extend(flat_ads)
    log.info(f"Found {len(flat_ads)} new flat ad{'s' if len(flat_ads) > 1 else ''}.") if len(flat_ads) else None
    log.debug(pformat(flat_ads))
    return flat_ads


def _parse_flat_ads(html: str) -> list[FlatAd]:
    page = BeautifulSoup(html, features="html.parser")
    flat_ads = []
    for div in page.select("#main_content .wgg_card.offer_list_item"):
        printonly_div = div.div.select_one("div .printonly")
        url = f'{WG_GESUCHT_BASE_URL}{printonly_div.a["href"]}'
        online_since = div.select_one("span[style*='color: #218700;']")
        online_since = online_since.text if online_since else ""
        uploaded_recently = any(word in online_since for word in ["Sekunde", "Minute"])
        if "asset_id" not in url and uploaded_recently:  # ignore ads
            info_divs = printonly_div.find_all("div")
            roommates = int(info_divs[1].text.strip()[0])
            free_from = datetime.strptime(info_divs[2].text.strip(), "Verfügbar: %d.%m.%Y").date()
            rent = int(info_divs[0].find_all("b")[0].text.split(" ")[0])
            size = int(info_divs[0].find_all("b")[1].text.strip()[:-2])
            district = info_divs[1].text.split("|")[1].split(" ")[-2]
            description = _get_flat_description(url)
            if uploaded_recently and rent > 100 and size < 30:
                flat_ads.append(FlatAd(url, roommates, rent, size, district, free_from, description))
    return [ad for ad in flat_ads if ad not in scraped_flat_ads]


@backoff.on_exception(backoff.expo, PageRenderError)
def _get_flat_description(url):
    details_html = requests_get(url).text
    details_page = BeautifulSoup(details_html, features="html.parser")
    headline = details_page.select_one(".headline-detailed-view-title")
    if not headline:
        raise PageRenderError("Could not render detail page!")
    headline_text = headline.text.strip()
    description_divs = details_page.select("div[id^='freitext']")
    description = "\n".join([div.text.strip() for div in description_divs])
    return f'{headline_text}\n{description}'
