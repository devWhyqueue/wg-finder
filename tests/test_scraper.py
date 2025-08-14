from wgfinder.scraper import _get_flat_description


def test_get_flat_description():
    url = "https://www.wg-gesucht.de/wg-zimmer-in-Berlin-Prenzlauer-Berg.10422146.html"
    description = _get_flat_description(url)
    # print(description)
