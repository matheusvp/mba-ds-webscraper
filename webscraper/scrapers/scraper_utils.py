from requests_html import HTMLSession
import requests as _requests


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
    return r.html