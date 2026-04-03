from types import SimpleNamespace

from wgfinder import scraper


def test_get_flat_description(monkeypatch):
    html = """
    <div class="detailed-view-title">
      <span class="foo">ignore</span>
      <span class="bar">Bright room in Prenzlauer Berg</span>
    </div>
    <div id="freitext_0">Large furnished room.</div>
    <div id="freitext_1">Close to public transport.</div>
    """
    monkeypatch.setattr(
        scraper, "requests_get", lambda url: SimpleNamespace(text=html)
    )

    url = "https://www.wg-gesucht.de/wg-zimmer-in-Berlin-Prenzlauer-Berg.10422146.html"
    description = scraper._get_flat_description(url)

    assert description == (
        "Bright room in Prenzlauer Berg\n"
        "Large furnished room.\n"
        "Close to public transport."
    )


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
