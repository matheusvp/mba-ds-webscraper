import webscraper.scrapers.scraper_8itempregare as _scraper_8itempregare
import webscraper.scrapers.scraper_trampos as _scraper_trampos
import webscraper.scrapers.scraper_programathor as _scraper_programathor
import webscraper.scrapers.scraper_geekhunter as _scraper_geekhunter
import webscraper.scrapers.data_wrangling as _data_wrangling
import toml
import sys
import csv


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


def obter_todos_dados():
    dados = []
    dados_tpm = obter_dados_geekhunter()
    if dados_tpm is not None and len(dados_tpm) > 0:
        dados += dados_tpm

    dados_tpm = obter_dados_8itempregare()
    if dados_tpm is not None and len(dados_tpm) > 0:
        dados += dados_tpm

    dados_tpm = obter_dados_programathor()
    if dados_tpm is not None and len(dados_tpm) > 0:
        dados += dados_tpm

    dados_tpm = obter_dados_trampos()
    if dados_tpm is not None and len(dados_tpm) > 0:
        dados += dados_tpm

    if len(dados) <= 0:
        return None

    return dados


def tratar_dados(vagas):
    return _data_wrangling.tratar_vagas(vagas)


def gravar_dados(dados):
    with open(CONFIG["arquivo"]["caminho"], "w") as stream:
        writer = csv.writer(stream, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(CONFIG["arquivo"]["cabecalho"])
        writer.writerows(dados)


def app():

    # Extrair dados
    print("Iniciando extração de dados...")
    dados = obter_todos_dados()

    # Se nenhum for extraído com sucesso termina o programa
    if dados is None:
        print("NENHUM dado extraído com sucesso")
        sys.exit()

    # trata os dados
    print("#########################################################")
    print("Iniciando tratamento dos dados...")
    dados = tratar_dados(dados)

    # grava os dados em um arquivo csv
    print("#########################################################")
    print("Gravando os dados no arquivo...")
    gravar_dados(dados)


if __name__ == "__main__":
    app()
