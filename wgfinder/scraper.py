import logging
from datetime import datetime
from pprint import pformat

import requests
from bs4 import BeautifulSoup

from wgfinder.models import FlatAd

WG_GESUCHT_SEARCH_URL = "https://www.wg-gesucht.de/wg-zimmer-in-Berlin.8.0.0.0.html?offer_filter=1&city_id=8&noDeact" \
                        "=1&dTo=1648677600&categories%5B%5D=0&rent_types%5B%5D=2&sMin=18&rMax=600&wgSea=2&wgMnF=2" \
                        "&wgMxT=4&wgArt%5B%5D=12&wgArt%5B%5D=1&wgArt%5B%5D=11&wgArt%5B%5D=19&wgArt%5B%5D=16&wgArt%5B" \
                        "%5D=15&wgArt%5B%5D=7&wgArt%5B%5D=5&wgArt%5B%5D=13&wgArt%5B%5D=22"
log = logging.getLogger(__name__)


def find_shared_flats() -> set[FlatAd]:
    html = requests.get(WG_GESUCHT_SEARCH_URL).text
    page = BeautifulSoup(html, features="html.parser")
    flat_ads = set()
    for row in page.table.tbody.find_all("tr"):
        cols = row.find_all("td")
        uploaded = datetime.strptime(cols[2].a.span.text.strip(), "%d.%m.%Y").date()
        rent = cols[3].a.span.b.text.strip().rstrip("€")
        size = cols[4].a.span.text.strip()[:-2]
        district = " ".join(cols[5].a.span.text.strip().split())
        free_from = datetime.strptime(cols[6].a.span.text.strip(), "%d.%m.%Y").date()
        # TODO: Parse url and roommates
        flat_ads.add(FlatAd("https://google.com", 4, uploaded, rent, size, district, free_from))
    flat_ads = {ad for ad in flat_ads if ad.uploaded_today() and ad.not_advertising()
                and ad.free_from.month in range(2, 5)}
    log.debug(pformat(flat_ads))
    return flat_ads
