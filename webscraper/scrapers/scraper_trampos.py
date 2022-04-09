import webscraper.scrapers.scraper_utils as _utils
from webscraper.scrapers.vaga import Vaga
from requests_html import HTMLSession
import json




def obter_dados(CONFIG):
    """ Retorna um array com os dados das vagas do site trampos """
    # Msg de inicialização
    print("Iniciando extração de dados de trampos.co.")

    # Obtêm a lista de urls das vagas
    lista_url_das_vagas = _obter_lista_url_das_vagas(CONFIG)

    if lista_url_das_vagas is None:
        return None

    # Extrai a informação das vagas
    vagas = _processar_vagas(lista_url_das_vagas)
    return vagas


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
    dados_json = json.loads(dados_raw) if dados_raw is not None else None

    # Para se a request para a url de listagem nao retornar nada
    # Ou se ela retornar opportunities: [] (se eu chamo uma pagina que nao existe dados esse é o comportamento
    # Ou ainda se ja tivermos capturado 100 vagas
    while dados_raw is not None and len(dados_json.get("opportunities")) > 0 and len(lista_url_vagas) < ponto_parada:
        print(f"Buscando vagas na url: {url}")
        for vaga in dados_json.get("opportunities"):
            if len(lista_url_vagas) < ponto_parada:
                lista_url_vagas.append(url_base + "/" + str(vaga.get("id")))
        page += 1
        url = _utils.montar_url(url_listagem, page)
        dados_raw = _utils.get_dados(url)
        dados_json = json.loads(dados_raw)

    print(f"Total de vagas capturadas: {len(lista_url_vagas)}")
    print(f"Lista de vagas capturadas: {lista_url_vagas}")
    if len(lista_url_vagas) == 0:
        return None

    return lista_url_vagas


def _processar_vagas(lista_url_das_vagas):
    """ A partir da lista de url das vagas, acessa uma a uma e extrai as informações relevantes """

    vaga = Vaga()

    #dados = _utils.get_dados(lista_url_das_vagas[0])
    #soup = BeautifulSoup(dados, 'html.parser')
    #print(soup.find_all("div", class_="container-titulo-vaga")])

    #dados = _utils.get_dados("https://trampos.co/oportunidades/728693")
    #soup = BeautifulSoup(dados, 'html.parser')
    #print(soup.find_all("div", class_="container-titulo-vaga")])
    #print(dados)

    dados = _utils.get_dados("https://trampos.co/oportunidades/728693")
    r = _utils.render_dados("https://trampos.co/oportunidades/728693")

    print(type(dados))
    print(dados)
    #print(str(r.raw_html))



    return 1