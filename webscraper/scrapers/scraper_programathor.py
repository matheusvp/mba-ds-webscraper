import webscraper.scrapers.scraper_utils as _utils
from bs4 import BeautifulSoup


def obter_dados(CONFIG):
    """ Retorna um array com os dados das vagas do site 8itempregare """
    # Msg de inicialização
    print("Iniciando extração de dados de programathor.")

    # Obtêm a lista de urls das vagas
    lista_url_das_vagas = _obter_lista_url_das_vagas(CONFIG)

    if lista_url_das_vagas is None:
        return None

    # Extrai a informação das vagas
    # vagas = _processar_vagas(lista_url_das_vagas)
    # return vagas
    return None


def _obter_lista_url_das_vagas(CONFIG):
    """ Retorna um array com as urls de cada vaga """
    # Carrega as configs
    page = CONFIG["pagina_inicial"]
    url_listagem = CONFIG["url_listagem"]
    url_base = CONFIG["url_base"]
    ponto_parada = CONFIG["parar_apos_x_vagas"]

    # Monta a url
    url = _utils.montar_url(url_listagem, page)

    # Busca a lista de vagas
    lista_url_vagas = []
    dados_raw = _utils.get_dados(url)
    dados_bs = BeautifulSoup(dados_raw, 'html.parser')
    div_tags = dados_bs.find_all('div', class_="cell-list")

    # Para se a request para a url de listagem nao retornar nada
    # Ou se ela nao conter dados (div_tags)
    # Ou ainda se ja tivermos capturado 100 vagas
    while dados_raw is not None and len(div_tags) > 0 and len(lista_url_vagas) < ponto_parada:
        print(f"Buscando vagas na url: {url}")
        for a_tag in div_tags:
            if a_tag.find('a') is not None and len(lista_url_vagas) < ponto_parada:
                lista_url_vagas.append(url_base + a_tag.find('a').get('href'))
        page += 1
        url = _utils.montar_url(url_listagem, page)
        dados_raw = _utils.get_dados(url)
        dados_bs = BeautifulSoup(dados_raw, 'html.parser')
        div_tags = dados_bs.find_all('div', class_="cell-list")

    print(f"Total de vagas capturadas: {len(lista_url_vagas)}")
    print(f"Lista de vagas capturadas: {lista_url_vagas}")
    if len(lista_url_vagas) == 0:
        return None

    return lista_url_vagas
