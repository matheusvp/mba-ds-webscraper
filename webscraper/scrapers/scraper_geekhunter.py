import webscraper.scrapers.scraper_utils as _utils
from bs4 import BeautifulSoup

from webscraper.scrapers.vaga import Vaga
from datetime import date


def obter_dados(CONFIG):
    """ Retorna um array de Vagas com os dados do site geekhunter """
    # Msg de inicialização
    print("Iniciando extração de dados de geekhunter.")

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
    div_tags = dados_bs.find_all('div', class_="job")

    # Para se a request para a url de listagem nao retornar nada
    # Ou se ela nao conter dados (div_tags)
    # Ou ainda se ja tivermos capturado 100 vagas
    while dados_raw is not None and len(div_tags) > 0 and len(lista_url_vagas) < ponto_parada:
        print(f"Buscando vagas na url: {url}")
        for a_tag in div_tags:
            if a_tag.find('h2') is not None and a_tag.find('a') is not None and len(lista_url_vagas) < ponto_parada:
                lista_url_vagas.append(url_base + a_tag.find('h2').find('a').get('href'))
        page += 1
        url = _utils.montar_url(url_listagem, page)
        dados_raw = _utils.get_dados(url)
        dados_bs = BeautifulSoup(dados_raw, 'html.parser')
        div_tags = dados_bs.find_all('div', class_="job")

    print(f"Total de vagas capturadas: {len(lista_url_vagas)}")
    # print(f"Lista de vagas capturadas: {lista_url_vagas}")
    if len(lista_url_vagas) == 0:
        return None

    return lista_url_vagas


def _processar_vagas(lista_url_das_vagas):
    """ A partir da lista de url das vagas, acessa uma a uma e extrai as informações relevantes
        retornando um array de Vagas"""

    i = 1
    vagas = []
    for url in lista_url_das_vagas:
        print(f"Processando vaga {i} de {len(lista_url_das_vagas)}")
        vaga = _processar_vaga(url)
        if vaga is not None:
            vagas.append(vaga)
        i += 1

    return vagas


def _processar_vaga(url):
    """ A partir de uma pagina html de uma vaga e da url extrai os dados da vaga"""

    dados_raw = _utils.get_dados(url)
    dados_bs = BeautifulSoup(dados_raw, 'html.parser')
    main_card = dados_bs.find("div", class_="main-card")
    full_description = dados_bs.find("div", class_="col-lg-8 full-description")
    vaga = Vaga()

    # Se não encontrar o main-card ou full description não temos dados da vaga então não retornamos a mesma (None)
    if main_card is None or full_description is None:
        return None

    # Dados que não existem nesse website
    vaga.id = "N/A"
    vaga.url = url
    vaga.data_scraping = date.today().strftime("%Y-%m-%d")
    vaga.data_publicacao = "N/A"
    vaga.empresa = "N/A"
    vaga.descricao = "N/A"

    # Captura cada uma das informações da vaga a partir da pagina web
    vaga.titulo = _processar_titulo(main_card)
    vaga.local_trabalho = _processar_local_trabalho(main_card)
    vaga.responsabilidades = _processar_responsabilidades(full_description)
    vaga.salario = _processar_salario(main_card)
    vaga.beneficios = _processar_beneficios(full_description)
    vaga.requisitos = _processar_requisitos(full_description)

    return vaga


def _processar_titulo(main_card):
    div_header = main_card.find("div", class_="card-header")

    # Se nao localizar a tag retorna N/A
    if div_header is None:
        return "N/A"

    h1_tag = div_header.find("h1")

    # Se nao localizar a tag retorna N/A
    if h1_tag is None:
        return "N/A"

    # Retorna titulo
    return h1_tag.getText()


def _processar_local_trabalho(main_card):
    span_local = main_card.find("i", class_="material-icons-outlined").parent

    # Se nao localizar a tag retorna N/A
    if span_local is None:
        return "N/A"

    span_remoto = span_local.find("span", class_="badge badge-secondary badge-remote")

    if span_remoto is None:
        if len(span_local.findAll(text=True, recursive=False)) > 1:
            return span_local.findAll(text=True, recursive=False)[1].strip()
        else:
            return span_local.findAll(text=True, recursive=False)[0].strip()
    else:
        return "Remoto"


def _processar_responsabilidades(full_description):
    div_activities = full_description.find("div", class_="activities")

    # Se nao localizar a tag retorna N/A
    if div_activities is None:
        return "N/A"

    div_descricao = div_activities.find("div", class_="col-md-12")

    # Se nao localizar a tag retorna N/A
    if div_descricao is None:
        return "N/A"

    return div_descricao.getText().strip()


def _processar_salario(main_card):
    span_salario = main_card.find("img", alt="Money")

    # Se nao localizar a tag retorna N/A
    if span_salario is None:
        return "N/A"

    span_salario = span_salario.parent

    # Retorna Salario
    return span_salario.get_text().replace("\n", "")


def _processar_beneficios(full_description):
    beneficios = ""
    div_beneficios = full_description.find_all("div", class_="col-lg-4 col-md-4 benefit")

    if len(div_beneficios) <= 0:
        return "N/A"

    for div_beneficio in div_beneficios:
        strong = div_beneficio.strong
        if strong is None:
            beneficios += ""
        beneficios += strong.get_text()
        beneficios += ";"

    beneficios.replace(";;", ";").replace(".;", ";").replace(":;", ";")
    return beneficios


def _processar_requisitos(full_description):
    div_activities = full_description.find("div", class_="activities", id="anchor-requirements")

    # Se nao localizar a tag retorna N/A
    if div_activities is None:
        return "N/A"

    div_row = div_activities.find("div", class_="row")
    # Se nao localizar a tag retorna N/A
    if div_row is None:
        return "N/A"

    div_beneficios = div_row.find("div", class_="col-md-12")
    # Se nao localizar a tag retorna N/A
    if div_beneficios is None:
        return "N/A"

    return div_beneficios.get_text(strip=True, separator=";").replace(";;", ";").replace(".;", ";").replace(":;", ";")
