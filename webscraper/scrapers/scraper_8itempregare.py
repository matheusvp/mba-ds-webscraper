import webscraper.scrapers.scraper_utils as _utils
from webscraper.scrapers.vaga import Vaga
from bs4 import BeautifulSoup
import json


def obter_dados(CONFIG):
    """ Retorna um array com os dados das vagas do site 8itempregare """
    # Msg de inicialização
    print("Iniciando extração de dados de 8itempregare.")

    # Obtêm a lista de urls das vagas
    lista_url_das_vagas = _obter_lista_url_das_vagas(CONFIG)

    if lista_url_das_vagas is None:
        return None

    # Extrai a informação das vagas
    #vagas = _processar_vagas(lista_url_das_vagas)
    #return vagas
    return None


def _obter_lista_url_das_vagas(CONFIG):
    """ Retorna um array com as urls de cada vaga """
    # Carrega as configs
    page = CONFIG["pagina_inicial"]
    url_listagem = CONFIG["url_listagem"]
    url_base = CONFIG["url_base"]
    ponto_parada = CONFIG["parar_apos_x_vagas"]

    #Monta a url
    url = _utils.montar_url(url_listagem, page)

    # Busca a lista de vagas
    lista_url_vagas = []
    dados_raw = _utils.get_dados(url)
    dados_json = json.loads(dados_raw) if dados_raw is not None else None

    # Para se a request para a url de listagem nao retornar nada
    # Ou se ela retornar dados: [] (se eu chamo uma pagina que nao existe dados esse é o comportamento
    # Ou ainda se ja tivermos capturado 100 vagas
    while dados_raw is not None and len(dados_json.get("dados")) > 0 and len(lista_url_vagas) < ponto_parada:
        print(f"Buscando vagas na url: {url}")
        for vaga in dados_json.get("dados"):
            if len(lista_url_vagas) < ponto_parada:
                lista_url_vagas.append(url_base + "/" + vaga.get("url"))
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

    url1 = "https://8it.empregare.com/pt-br/vaga-desenvolvedor-net-core-pleno_22646"
    url2 = "https://8it.empregare.com/pt-br/vaga-banco-de-talentos-profissionais-de-ti_22488"
    _processar_vaga(url1)

    return 1

def _processar_vaga(url):
    """ A partir de uma pagina html de uma vaga e da url extrai os dados da vaga"""

    dados_raw = _utils.get_dados(url)
    dados_bs = BeautifulSoup(dados_raw, 'html.parser')
    div_container_titulo = dados_bs.find("div", class_="container-fluid bg-gradient container-titulo-vaga")
    div_container_detalhes = dados_bs.find("div", class_="col-md-9 container-detalhes-vaga")
    vaga = Vaga()

    # Se não encontrar o main-card ou full description não temos dados da vaga então não retornamos a mesma (None)
    if div_container_titulo is None or div_container_detalhes is None:
        return None

    # Dados que não existem nesse website
    vaga.id = "N/A"
    vaga.url = url
    vaga.data_scraping = date.today().strftime("%Y-%m-%d")
    # vaga.data_publicacao = "N/A"
    # vaga.empresa = "N/A"
    # vaga.descricao = "N/A"

    # Captura cada uma das informações da vaga a partir da pagina web
    # vaga.titulo = _processar_titulo(main_card)
    # vaga.local_trabalho = _processar_local_trabalho(main_card)
    # vaga.responsabilidades = _processar_responsabilidades(full_description)
    # vaga.salario = _processar_salario(main_card)
    # vaga.beneficios = _processar_beneficios(full_description)
    # vaga.requisitos = _processar_requisitos(full_description)

    return vaga