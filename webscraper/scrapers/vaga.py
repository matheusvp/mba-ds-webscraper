class Vaga:
    def __init__(self):
        self.id = "N/A"
        self.url = "N/A"
        self.data_scraping = "N/A"
        self.data_publicacao = "N/A"
        self.titulo = "N/A"
        self.empresa = "N/A"
        self.local_trabalho = "N/A"
        self.responsabilidades = "N/A"
        self.requisitos = "N/A"
        self.salario = "N/A"
        self.modelo_contratacao = "N/A"
        self.beneficios = "N/A"

    def __repr__(self):
        return f"Vaga({self.id!r}, {self.url!r}, {self.data_scraping!r}, {self.data_publicacao!r}, {self.titulo!r}" \
               f", {self.empresa!r}, {self.local_trabalho!r}, {self.responsabilidades!r}, {self.requisitos!r}" \
               f", {self.salario!r}, {self.modelo_contratacao!r}, {self.beneficios!r})"

    def __iter__(self):
        return iter([self.id, self.url, self.data_scraping, self.data_publicacao, self.titulo, self.empresa,
                     self.local_trabalho, self.responsabilidades, self.requisitos, self.salario,
                     self.modelo_contratacao, self.beneficios])
