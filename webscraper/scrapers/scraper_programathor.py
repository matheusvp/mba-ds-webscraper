import requests as _requests

def test():
    r1 = _requests.get('https://programathor.com.br/jobs/page/1')
    r2 = _requests.get('https://8it.empregare.com/api/pt-br/vagas/buscar?Pag=1&q=&empresa=QdOcUw7QEYA%7C&hotSiteUrl=8it&carregarFiltro=true&carregarLista=true')  # precisa de js
    r3 = _requests.get('https://www.geekhunter.com.br/vagas?page=1')
    r4 = _requests.get('https://trampos.co/api/v2/opportunities?lc=&tr=desenvolvedor&page=1')
    print(r2.text)