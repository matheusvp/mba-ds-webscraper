# Webscraper

Um web scraper feito em Python para captura de dados de vagas de desenvolvedores de software.


## Installation

Esse projeto utiliza Poetry. Para informações sobre como instalar o Poetry, procure a [documentação oficial](https://python-poetry.org/docs/#installation). Para instalar o projeto use o comando abaixo no root do projeto:

```bash
  poetry install
```
   
## Configuração

O arquivo *config.toml* contém a configuração do projeto. Por favor, altere o parâmetro do arquivo de saida com um caminho e nome adequado para você.

```bash
  arquivo="/tmp/output.csv"
```


## Usage/Examples

O comando abaixo executa o projeto:

```python
  poetry run start
```

Esse comando nada mais é do que a execução da função app do arquivo webscraper/main.py
## Authors

- [@matheusvp](https://github.com/matheusvp)
