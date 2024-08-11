import random

import backoff
import requests

WEBSHARE_PROXIES = ("https://proxy.webshare.io/api/v2/proxy/list/download/owiebmhtlkuzgkodphekgzkftqxgeruyhoayjpmu"
                    "/-/any/username/direct/-/")
webshare_proxies = []
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
]


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
def requests_get(url):
    global webshare_proxies
    webshare_proxies = webshare_proxies if len(webshare_proxies) else _get_proxies()
    headers = {'User-Agent': random.choice(user_agents)}
    response = requests.get(url, proxies={"https": random.choice(webshare_proxies)}, headers=headers,
                            timeout=5, allow_redirects=False)
    return requests_get(url) if response.status_code == 302 else response


def _get_proxies() -> list[str]:
    proxies = []
    for proxy in requests.get(WEBSHARE_PROXIES).text.splitlines():
        address = proxy.split(":")
        proxies.append(f"http://{address[2]}:{address[3]}@{address[0]}:{address[1]}")
    return proxies
