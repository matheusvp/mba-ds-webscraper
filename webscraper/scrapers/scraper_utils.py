from requests_html import HTMLSession
import requests as _requests
from datetime import date


def montar_url(url, page):
    return url.format(page=page)


def get_dados(url):
    try:
        r = _requests.get(url)
        if r.status_code != 200:
            return None
        else:
            return r.text
    except:
        print(f"Não foi possível obter os dados da url: {url}")
        return None


def render_dados(url):
    try:
        s = HTMLSession()
        r = s.get(url)
        r.html.render()
        return r.html.raw_html
    except:
        print(f"Não foi possível obter os dados da url: {url}")
        return None


def get_data_hoje():
    return date.today().strftime("%Y%m%d")
