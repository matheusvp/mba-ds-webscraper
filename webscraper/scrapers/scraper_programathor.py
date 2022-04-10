import webscraper.scrapers.scraper_utils as _utils
from bs4 import BeautifulSoup

from webscraper.scrapers.vaga import Vaga


def obter_dados(CONFIG):
    """ Retorna um array com os dados das vagas do site 8itempregare """
    # Msg de inicialização
    print("Iniciando extração de dados de programathor.")

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
    # print(f"Lista de vagas capturadas: {lista_url_vagas}")
    if len(lista_url_vagas) == 0:
        return None

    return lista_url_vagas


def _processar_vagas(lista_url_das_vagas):
    """ A partir da lista de url das vagas, acessa uma a uma e extrai as informações relevantes
        retornando um array de Vagas"""

    if len(lista_url_das_vagas) <= 0:
        return None

    i = 1
    vagas = []
    for url in lista_url_das_vagas:
        print(f"Processando vaga {i} de {len(lista_url_das_vagas)}")
        vaga = _processar_vaga(url)
        if vaga is not None:
            vagas.append(vaga)
        i += 1

    if len(vagas) <= 0:
        return None

    return vagas

def _processar_vaga(url):
    """ A partir de uma pagina html de uma vaga e da url extrai os dados da vaga"""

    dados_raw = _utils.get_dados(url)
    if dados_raw is None:
        return None
    dados_bs = BeautifulSoup(dados_raw, 'html.parser')
    div_titulo = dados_bs.find("div", class_="wrapper-header-job-show background-blue text-center")
    div_cabecalho = dados_bs.find("div", class_="wrapper-content-job-show")
    div_corpo = dados_bs.find("div", class_="line-height-2-4")
    vaga = Vaga()

    # Se não encontrar os dados não temos dados da vaga então não retornamos a mesma (None)
    if div_cabecalho is None or div_corpo is None or div_titulo is None:
        return None

    # Dados que não existem nesse website
    vaga.id = "N/A"
    vaga.url = url
    vaga.data_scraping = _utils.get_data_hoje()
    vaga.data_publicacao = "N/A"

    # Captura cada uma das informações da vaga a partir da pagina web
    vaga.titulo = _processar_titulo(div_titulo)
    vaga.empresa = _processar_empresa(div_cabecalho)
    vaga.local_trabalho = _processar_local_trabalho(dados_bs)
    vaga.responsabilidades = _processar_responsabilidades(div_corpo)
    vaga.salario = _processar_salario(div_cabecalho)
    vaga.modelo_contratacao = _processar_modelo_contratação(div_cabecalho)
    vaga.beneficios = _processar_beneficios(div_corpo)
    vaga.requisitos = _processar_requisitos(div_corpo)

    return vaga


def _processar_titulo(div_titulo):
    tag_h1 = div_titulo.find("h1")
    if tag_h1 is None:
        return "N/A"

    return tag_h1.get_text(strip=True)


def _processar_empresa(div_cabecalho):
    tag_h2 = div_cabecalho.find("h2")
    if tag_h2 is None:
        return "N/A"

    return tag_h2.get_text(strip=True)


def _processar_local_trabalho(dados_bs):
    tag_ol = dados_bs.find("ol", class_="breadcrumb background-white")
    if tag_ol is None:
        return "N/A"

    tags_li = tag_ol.find_all("li")
    if len(tags_li) < 3:
        return "N/A"

    return tags_li[2].get_text(strip=True)


def _processar_salario(div_cabecalho):
    tag_i = div_cabecalho.find("i", class_="far fa-money-bill-alt")
    if tag_i is None:
        return "N/A"

    tag_span = tag_i.parent
    if tag_span is None:
        return "N/A"

    tag_p = tag_span.parent
    if tag_i is None:
        return "N/A"

    salario = tag_p.get_text(strip=True)
    pos = salario.find(":")
    if pos != -1:
        salario = salario[pos+1:]
    return salario.strip()


def _processar_modelo_contratação(div_cabecalho):
    tag_i = div_cabecalho.find("i", class_="far fa-file-alt")
    if tag_i is None:
        return "N/A"

    tag_span = tag_i.parent
    if tag_span is None:
        return "N/A"

    tag_p = tag_span.parent
    if tag_i is None:
        return "N/A"

    return tag_p.get_text(strip=True,separator=";")


def _processar_responsabilidades(div_corpo):
    tag_h3 = div_corpo.find("h3", string="Atividades e Responsabilidades")
    if tag_h3 is None:
        return "N/A"

    tag_div = tag_h3.find_next_siblings("p")
    if len(tag_div) < 1:
        return "N/A"

    tag_p = tag_div[0]
    if tag_p is None:
        return "N/A"

    return tag_p.get_text(strip=True, separator=";")


def _processar_requisitos(div_corpo):
    tag_h3 = div_corpo.find("h3", string="Requisitos")
    if tag_h3 is None:
        return "N/A"

    tag_div = tag_h3.find_next_siblings("p")
    if len(tag_div) < 1:
        return "N/A"

    tag_p = tag_div[0]
    if tag_p is None:
        return "N/A"

    return tag_p.get_text(strip=True, separator=";")


def _processar_beneficios(div_corpo):
    tag_div = div_corpo.find("div", class_="background-gray padding-small-full")
    if tag_div is None:
        return "N/A"

    return tag_div.get_text(strip=True, separator=";")