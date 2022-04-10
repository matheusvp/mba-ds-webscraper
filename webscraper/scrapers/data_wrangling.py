def _ajustar_ids(vagas):
    i = 1
    for vaga in vagas:
        vaga.id = i
        i += 1
    return vagas


def _limpar_quebra_de_linha(string):
    """ Recebe uma string e limpa quebra de linha e tabulação"""
    return string.replace("\r\n", "").replace("\n", "").replace("\t", "").replace("\r", "")


def _ajustar_separadores(string):
    """ Recebe uma string e ajusta os separadores que podem estar duplicados/incorretos devido a extração"""
    string = string.replace(";;", ";").replace(".;", ";").replace(":;", ";").replace("•", "")
    string = string.replace("; ", ";").replace("-", "").strip()
    return string


def _ajustar_ultimo_charactere(string):
    if string[-1] == "." or string[-1] == "!" or string[-1] == ";" or string[-1] == ":":
        string = string[:-1]
    return string


def _limpar_caracteres_indesejaveis(vagas):
    """ Recebe uma lista de vagas e aplica _limpar_quebra_de_linha e _ajustar_separadores nos campos adequados"""
    for vaga in vagas:
        vaga.data_publicacao = _ajustar_separadores(_limpar_quebra_de_linha(vaga.data_publicacao))
        vaga.titulo = _ajustar_separadores(_limpar_quebra_de_linha(vaga.titulo))
        vaga.empresa = _ajustar_separadores(_limpar_quebra_de_linha(vaga.empresa))
        vaga.local_trabalho = _ajustar_separadores(_limpar_quebra_de_linha(vaga.local_trabalho))
        vaga.responsabilidades = _ajustar_separadores(_limpar_quebra_de_linha(vaga.responsabilidades))
        vaga.requisitos = _ajustar_separadores(_limpar_quebra_de_linha(vaga.requisitos))
        vaga.salario = _ajustar_separadores(_limpar_quebra_de_linha(vaga.salario))
        vaga.modelo_contratacao = _ajustar_separadores(_limpar_quebra_de_linha(vaga.modelo_contratacao))
        vaga.beneficios = _ajustar_separadores(_limpar_quebra_de_linha(vaga.beneficios))

        vaga.responsabilidades = _ajustar_ultimo_charactere(vaga.responsabilidades)
        vaga.requisitos = _ajustar_ultimo_charactere(vaga.requisitos)
        vaga.beneficios = _ajustar_ultimo_charactere(vaga.beneficios)
        vaga.local_trabalho = _padronizar_local_trabalho(vaga.local_trabalho)

    return vagas


def _padronizar_local_trabalho(string):
    if string == "remoto" or string == "Totalmente Remoto" or string == "Home office":
        string = "Remoto"
    return string


def _padronizar_modelo_contratacao(string):
    if string == "Prestador de Serviços  PJ" or string == "PREST. DE SERVIÇO":
        string = "PJ"
    if string == "INDIFERENTE":
        string = "CLT;PJ"
    return string


def _padronizar_salario(string):
    # Padronizar no formato R$ 4.000,00 R$ 6.000,00

    # Casos "R$ 11.900,00 R$ 13.800,00"
    string = string.replace("0 R$", "0 até R$")

    # Casos "R$ 3.500 a R$ 4.500"
    string = string.replace("0 a R$", "0 até R$")

    return string


def _padronizar_dados(vagas):
    """ Recebe uma lista de vagas e padroniza os valores de alguns campos"""
    for vaga in vagas:
        vaga.local_trabalho = _padronizar_local_trabalho(vaga.local_trabalho)
        vaga.modelo_contratacao = _padronizar_modelo_contratacao(vaga.modelo_contratacao)
        vaga.salario = _padronizar_salario(vaga.salario)

    return vagas


def tratar_vagas(vagas):
    """ Espera um array de vagas, adiciona o id, limpa caracteres indesejáveis e quebra de linha nos campos"""
    # remove possíveis entradas vazias (None)
    vagas = list(filter(None, vagas))

    # Ajusta os ids
    vagas = _ajustar_ids(vagas)

    # Limpa quebra de linha, caracteres indesejáveis e separadores duplicados
    vagas = _limpar_caracteres_indesejaveis(vagas)

    # padronização de dados
    vagas = _padronizar_dados(vagas)

    return vagas
