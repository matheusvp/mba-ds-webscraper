import webscraper.scrapers.scraper_8itempregare as _scraper_8itempregare
import webscraper.scrapers.scraper_trampos as _scraper_trampos
import webscraper.scrapers.scraper_programathor as _scraper_programathor
import webscraper.scrapers.scraper_geekhunter as _scraper_geekhunter
import toml


# Carrega arquivo de configuração
CONFIG = toml.load("config.toml")["app"]


def obter_dados_8itempregare():
    return _scraper_8itempregare.obter_dados(CONFIG['8itempregare'])


def obter_dados_trampos():
    return _scraper_trampos.obter_dados(CONFIG['trampos'])


def obter_dados_programathor():
    return _scraper_programathor.obter_dados(CONFIG['programathor'])


def obter_dados_geekhunter():
    return _scraper_geekhunter.obter_dados(CONFIG['geekhunter'])


def app():
    print("Iniciando extração de dados...")

    #obter_dados_8itempregare()
    #obter_dados_trampos()
    #obter_dados_programathor()

    # feitos
    obter_dados_geekhunter()


if __name__ == "__main__":
    app()
