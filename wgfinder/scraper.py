import logging
from datetime import datetime
from pprint import pformat

import requests
from bs4 import BeautifulSoup

from wgfinder.models import FlatAd

WG_GESUCHT_BASE_URL = "https://www.wg-gesucht.de"
WG_GESUCHT_SEARCH_QUERY = "wg-zimmer-in-Berlin.8.0.0.0.html?offer_filter=1&city_id=8&noDeact" \
                          "=1&dTo=1648677600&categories%5B%5D=0&rent_types%5B%5D=2&sMin=18&rMax=600&wgSea=2&wgMnF=2" \
                          "&wgMxT=4&wgArt%5B%5D=12&wgArt%5B%5D=1&wgArt%5B%5D=11&wgArt%5B%5D=19&wgArt%5B%5D=16&wgArt" \
                          "%5B%5D=15&wgArt%5B%5D=7&wgArt%5B%5D=5&wgArt%5B%5D=13&wgArt%5B%5D=22"
log = logging.getLogger(__name__)
scraped_flat_ads = set()


def find_shared_flats() -> set[FlatAd]:
    try:
        html = requests.get(f"{WG_GESUCHT_BASE_URL}/{WG_GESUCHT_SEARCH_QUERY}").text
        flat_ads = _parse_flat_ads(html)
        scraped_flat_ads.update(flat_ads)
        log.info(f"Found {len(flat_ads)} new flat ad{'s' if len(flat_ads) > 1 else ''}.") if len(flat_ads) else None
        log.debug(pformat(flat_ads))
        return flat_ads
    except ConnectionError:
        log.exception(f"Could not connect to server!")


def _parse_flat_ads(html: str) -> set[FlatAd]:
    page = BeautifulSoup(html, features="html.parser")
    flat_ads = set()
    for row in page.table.tbody.find_all("tr"):
        cols = row.find_all("td")
        roommates = len(cols[1].a.span.find_all("img"))
        url = f'{WG_GESUCHT_BASE_URL}/{cols[2].a["href"]}'
        uploaded = datetime.strptime(cols[2].a.span.text.strip(), "%d.%m.%Y").date()
        rent = int(cols[3].a.span.b.text.strip().rstrip("€"))
        size = int(cols[4].a.span.text.strip()[:-2])
        district = " ".join(cols[5].a.span.text.strip().split())
        free_from = datetime.strptime(cols[6].a.span.text.strip(), "%d.%m.%Y").date()
        flat_ads.add(FlatAd(url, roommates, uploaded, rent, size, district, free_from))
    return {ad for ad in flat_ads if ad.uploaded_today() and not ad.only_advertising() and not ad.too_cheap()
            and ad.free_from.month in range(2, 5) and ad not in scraped_flat_ads}
