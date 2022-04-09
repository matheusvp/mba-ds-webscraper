import json
import webscraper.scrapers.scraper_utils as _utils
from bs4 import BeautifulSoup
from webscraper.scrapers.vaga import Vaga


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

    dados_raw = _utils.render_dados(url)
    dados_bs = BeautifulSoup(dados_raw, 'html.parser')
    div_dados = dados_bs.find("div", class_="opportunity-body")
    vaga = Vaga()

    # Se não encontrar o main-card ou full description não temos dados da vaga então não retornamos a mesma (None)
    if div_dados is None:
        return None

    # Dados que não existem nesse website
    vaga.id = "N/A"
    vaga.url = url
    vaga.data_scraping = _utils.get_data_hoje()
    vaga.data_publicacao = "N/A"

    # Captura cada uma das informações da vaga a partir da pagina web
    vaga.titulo = _processar_titulo(div_dados)
    vaga.empresa = _processar_empresa(div_dados)
    vaga.local_trabalho = _processar_local_trabalho(div_dados)
    vaga.responsabilidades = _processar_responsabilidades(div_dados)
    vaga.salario = _processar_salario(div_dados)
    vaga.modelo_contratação = _processar_modelo_contratação(div_dados)
    vaga.beneficios = _processar_beneficios(div_dados)
    vaga.requisitos = _processar_requisitos(div_dados)

    return vaga


def _processar_titulo(div_dados):
    tag_h1 = div_dados.find("h1", class_="name")

    if tag_h1 is None:
        return "N/A"

    return tag_h1.get_text(strip=True)


def _processar_empresa(div_dados):
    tag_p = div_dados.find("p", class_="address")

    if tag_p is None:
        return "N/A"

    tag_a = tag_p.a
    if tag_a is None:
        return "N/A"

    return tag_a.get_text(strip=True)


def _processar_local_trabalho(div_dados):
    tag_p = div_dados.find("p", class_="address")

    if tag_p is None:
        return "N/A"

    local = tag_p.get_text(strip=True)
    pos_separador = local.find("|")

    if pos_separador == -1:
        return "N/A"

    local = local[pos_separador + 1:]
    return local


def _processar_responsabilidades(div_dados):
    tag_h3 = div_dados.find("h3", string="Descrição")
    if tag_h3 is None:
        return "N/A"

    tag_div_resp = tag_h3.find_next_sibling("div", class_="text")
    if tag_div_resp is None:
        return "N/A"

    return tag_div_resp.get_text(strip=True, separator=";")


def _processar_salario(div_dados):
    tag_div = div_dados.find("div", class_="numbers")
    if tag_div is None:
        return "N/A"

    tag_strong = div_dados.find("strong", string="Faixa salarial")
    if tag_strong is None:
        return "N/A"

    tag_span = tag_strong.find_next_sibling("span", class_="blog-description")
    if tag_span is None:
        return "N/A"

    salario = tag_span.get_text(strip=True)
    if salario == "NÃO DIVULGADA":
        return "N/A"

    return salario


def _processar_modelo_contratação(div_dados):
    tag_div = div_dados.find("div", class_="numbers")
    if tag_div is None:
        return "N/A"

    tag_strong = div_dados.find("strong", string="Contratação")
    if tag_strong is None:
        return "N/A"

    tag_span = tag_strong.find_next_sibling("span", class_="blog-description")
    if tag_span is None:
        return "N/A"

    return tag_span.get_text(strip=True)


def _processar_beneficios(div_dados):
    tag_h3 = div_dados.find("h3", string="Benefícios")
    if tag_h3 is None:
        return "N/A"

    tag_div = tag_h3.find_next_sibling("div", class_="text")
    if tag_div is None:
        return "N/A"

    return tag_div.get_text(strip=True, separator=";")


def _processar_requisitos(div_dados):
    tag_h3 = div_dados.find("h3", string="Requisitos")
    if tag_h3 is None:
        return "N/A"

    tag_div = tag_h3.find_next_sibling("div", class_="text")
    if tag_div is None:
        return "N/A"

    requisitos = tag_div.get_text(strip=True, separator=";")
    desejavel = _processar_requisitos_desejavel(div_dados)
    if desejavel != "N/A":
        requisitos += ";"
        requisitos += desejavel

    return requisitos


def _processar_requisitos_desejavel(div_dados):
    tag_h3 = div_dados.find("h3", string="Desejável")
    if tag_h3 is None:
        return "N/A"

    tag_div = tag_h3.find_next_sibling("div", class_="text")
    if tag_div is None:
        return "N/A"

    desejavel = "Desejável:"
    desejavel += tag_div.get_text(strip=True, separator=";")

    return desejavel
