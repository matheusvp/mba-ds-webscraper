from requests_html import HTMLSession
import requests as _requests
from datetime import date


def montar_url(url, page):
    return url.format(page=page)


def get_dados(url):
    r = _requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.text


def render_dados(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render()
    return r.html.raw_html


def get_data_hoje():
    return date.today().strftime("%Y%m%d")
