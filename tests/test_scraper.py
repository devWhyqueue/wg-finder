from wgfinder import scraper


def test_get_flat_description():
    url = "https://www.wg-gesucht.de/wg-zimmer-in-Berlin-Prenzlauer-Berg.10422146.html"
    description = scraper._get_flat_description(url)
    # print(description)


def test_get_search_url_uses_app_ini(tmp_path, monkeypatch):
    monkeypatch.setattr(
        scraper,
        "get_required_config",
        lambda section, option, allow_placeholder=False: {
            ("wg_gesucht", "base_url"): "https://example.com",
            ("wg_gesucht", "search_query"): "custom-search.html?foo=bar",
        }[(section, option)],
    )

    assert scraper._get_search_url() == "https://example.com/custom-search.html?foo=bar"
