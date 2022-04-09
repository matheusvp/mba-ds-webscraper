import webscraper.scrapers.scraper_utils as _utils
import json
from webscraper.scrapers.vaga import Vaga
from bs4 import BeautifulSoup



def obter_dados(CONFIG):
    """ Retorna um array com os dados das vagas do site 8itempregare """
    # Msg de inicialização
    print("Iniciando extração de dados de 8itempregare.")

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
    # print(f"Lista de vagas capturadas: {lista_url_vagas}")
    if len(lista_url_vagas) == 0:
        return None

    return lista_url_vagas


def _processar_vagas(lista_url_das_vagas):
    """ A partir da lista de url das vagas, acessa uma a uma e extrai as informações relevantes """

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
    vaga.data_scraping = _utils.get_data_hoje()
    vaga.empresa = "N/A"

    # Captura cada uma das informações da vaga a partir da pagina web
    vaga.data_publicacao = _processar_data_publicacao(div_container_detalhes)
    vaga.titulo = _processar_titulo(div_container_titulo)
    vaga.local_trabalho = _processar_local_trabalho(div_container_detalhes)
    vaga.responsabilidades = _processar_responsabilidades(div_container_detalhes)
    vaga.salario = _processar_salario(div_container_titulo)
    vaga.modelo_contratação = _processar_modelo_contratacao(div_container_detalhes)
    vaga.beneficios = _processar_beneficios(div_container_detalhes)
    vaga.requisitos = _processar_requisitos(div_container_detalhes)

    return vaga


def _processar_data_publicacao(div_container_detalhes):
    data_publicacao = "N/A"

    # É a terceura small tag da pagina
    tag_small = div_container_detalhes.find_all("small")

    if len(tag_small) < 3:
        return data_publicacao

    tag_b = tag_small[2].b
    if tag_b is None:
        return data_publicacao
    data_publicacao = tag_b.getText()
    return data_publicacao



def _processar_titulo(div_container_titulo):
    tag_div_titulo = div_container_titulo.find("div", class_="col-md-9 vaga-titulo")
    if tag_div_titulo is None:
        return "N/A"

    tag_h1 = tag_div_titulo.h1
    if tag_h1 is None:
        return "N/A"

    return tag_h1.get_text(strip=True)


def _processar_local_trabalho(div_container_detalhes):
    tag_ul = div_container_detalhes.find("ul", class_="list-unstyled list-localidade-vaga row")
    if tag_ul is None:
        return "N/A"

    tag_li = tag_ul.li
    if tag_li is None:
        return "N/A"

    return tag_li.get_text(strip=True)



def _processar_responsabilidades(div_container_detalhes):
    tag_div_desc = div_container_detalhes.find("div", class_="vaga-descricao")
    if tag_div_desc is None:
        return "N/A"

    return tag_div_desc.get_text(strip=True,separator=";")


def _processar_salario(div_container_titulo):
    tag_div_titulo = div_container_titulo.find("div", class_="col-md-9 vaga-titulo")
    if tag_div_titulo is None:
        return "N/A"

    tag_li = tag_div_titulo.find("li", class_="titulo-itens container-Salario")
    if tag_li is None:
        return "N/A"

    tag_span = tag_li.span
    if tag_span is None:
        return "N/A"

    salario = tag_span
    if salario == "Salário a combinar":
        salario = "N/A"
    return salario


def _processar_modelo_contratacao(div_container_detalhes):
    tag_div_regime = div_container_detalhes.find("div", class_="col-sm-4 container-RegimeContratacao")
    if tag_div_regime is None:
        return "N/A"

    tag_p = tag_div_regime.p
    if tag_p is None:
        return "N/A"

    return tag_p.get_text(strip=True)


def _processar_beneficios(div_container_detalhes):
    tag_div_desc = div_container_detalhes.find_all("div", class_="vaga-descricao")
    # Terceira div class_="vaga-descricao"
    if len(tag_div_desc) <3:
        return "N/A"

    beneficios = tag_div_desc[2].get_text(strip=True, separator=";")
    if beneficios == "Nenhum benefício informado":
        return "N/A"

    return beneficios


def _processar_requisitos(div_container_detalhes):
    tag_div_desc = div_container_detalhes.find_all("div", class_="vaga-descricao")
    # Terceira div class_="vaga-descricao"
    if len(tag_div_desc) < 2:
        return "N/A"

    beneficios = tag_div_desc[1].get_text(strip=True, separator=";")
    if beneficios == "Nenhum benefício informado":
        return "N/A"

    return tag_div_desc[1].get_text(strip=True, separator=";")
