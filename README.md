<h1 align="center">:oncoming_taxi: Aluguel de Carros REST API</h1>
<p align="center"><a href="https://github.com/quelcamara/aluguel-carros"><img src="https://img.shields.io/badge/languages-1-pink"></a> <a href="https://github.com/quelcamara/aluguel-carros/commits/master"><img src="https://img.shields.io/badge/last%20commit-november-red"></a></p>

<p align="center"> :construction: Concluído  :heavy_check_mark:</p>

# Tabela de Conteúdos
* [Sobre o projeto](#sobre-o-projeto)
* [Funcionalidades](#funcionalidades)
* [Tecnologias](#tecnologias)
* [Como executar o projeto](#como-executar-o-projeto)
  * [Pré-requisitos](#pré-requisitos)
  * [Configurações iniciais](#configurações-iniciais)
  * [Rodando o Backend (servidor)](#rodando-o-backend)
  * [Testando a aplicação com Swagger](#testando-a-aplicação-com-swagger)
* [Autora](#autora)

## :computer: Sobre o projeto
Aluguel de Carros é uma API REST para sistemas de locação de veículos.

Projeto desenvolvido para compor portfólio de desenvolvimento.

## ⚙️ Funcionalidades
A aplicação permite que os usuários realizem:

- [x] Interações com usuários:

  - [x] Cadastros de clientes e funcionários
  - [x] Login e logout
  - [x] Buscas personalizadas
  - [x] Exclusão de cadastros
- [x] Interações com marcas e veículos:

  - [x] Registro de marcas e veículos
  - [x] Buscas personalizadas
  - [x] Aluguel e retorno de veículos
  - [x] Exclusão de cadastros

## 🛠 Tecnologias
O projeto foi desenvolvido utilizando as seguintes ferramentas:
* [Python](https://www.python.org/downloads/) --versão: 3.7
* [Flask](https://www.fullstackpython.com/flask.html) --versão: 1.1
* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/installation/) --versão: 3.24
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/installation.html) --versão: 0.3
* [Flask-RESTful-Swagger](https://flask-restful-swagger.readthedocs.io/en/latest/articles/README.html) --versão: 0.2
* [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/) --versão: 2.4
* [SQLAlchemy](https://www.sqlalchemy.org/library.html#architecture) --versão: 1.3
* [MySQL Workbench](https://dev.mysql.com/downloads/) --versão: 8.0
* [SQLite](https://www.sqlite.org/about.html) --versão: 3.31
* [PyMySQL](https://pypi.org/project/PyMySQL/#installation) --versão: 0.10

## :rocket: Como executar o projeto
Este projeto foi desenvolvido em uma única parte contendo o Backend (para server) da aplicação.

Para rodar a aplicação, precisarão ser feitas algumas configurações iniciais na máquina.

:bulb: Para fins de teste dos endpoints, a aplicação de backend deverá estar sendo executada localmente.

### Pré-requisitos
Antes de começar, você precisará ter instalado em sua máquina o [Python](https://www.python.org/downloads/). Além desta ferramenta, caso deseje trabalhar com o código, também é recomendável ter um editor para códigos, como o [VSCode](https://code.visualstudio.com/); ou uma IDE Python, como o [PyCharm](https://www.jetbrains.com/pt-br/pycharm/download/#section=windows).

Será necessário, também, fazer dowload do projeto [aluguel-carros](https://github.com/quelcamara/aluguel-carros).

#### :wrench: Configurações iniciais
A app foi construída em cima de um ambiente virtual contendo os pacotes necessários para o funcionamento desta API. Para configurar um ambiente virtual e executar o código, no terminal/cmd:
```shell
# Acesse a pasta do projeto (insira o endereço completo)
$ cd C:\..\aluguel-carros-master

# Crie um ambiente virtual (utilizando python 3.7)
$ virtualenv venv --python=python3.7

# Acesse o ambiente virtual
$ venv\Scripts\activate.bat
```
Feito isso, o terminal indicará a inicialização do ambiente virtual inserindo `(venv)` na linha de comando. Seu terminal deverá aparecer da seguinte forma:
```shell
$ (venv) C:\..\aluguel-carros-master>_
```
Em seguida, instale os pacotes no ambiente virtual utilizando o `pip install`. Eles trabalharão junto com o python na execução do código:
```shell
$ pip install FLask
$ pip install Flask-RESTful
$ pip install Flask-JWT-Extended
$ pip install Flask-SQLAlchemy
$ pip install Flask-RESTful-Swagger
$ pip install PyMySQL
```
Com essas configurações, sua máquina estará apta para executar a aplicação.

#### :game_die: Rodando o Backend (servidor)
Para iniciar a aplicação:
* Com banco de dados SQLite:

  Caso não possua o MySQL instalado em sua máquina, é possível ter acesso ao código com o SQLite.
  
  Para isso, basta executar o código sem inserir nenhum parâmetro na linha de comando. O SQLite funcionará como banco de dados default.
```shell
$ python .\code\app.py
```
* Com banco de dados MySQL:
  
  Para executar com banco MySQL, você deverá criar um banco com nome `aluguelcarros_db`.
  
  Em seguida, basta inserir os parâmetros de entrada `--db=`, `--dbuser=` e `--dbpassword` na linha de comando.
  
  Nos campos `<USUÁRIO>` e `<SENHA>` devem ser inseridos os seus dados de acesso ao MySQL.
```shell
$ python .\code\app.py --db=mysql --dbuser=<USUÁRIO> --dbpassword=<SENHA>
```
O servidor iniciará em host=localhost e port=5000.

Acesse inserindo `http://localhost:5000/` na barra de endereços do seu browser, ou clicando [aqui](http://localhost:5000/).

#### :key:Testando a aplicação com Swagger
Todo o código desta aplicação encontra-se documentado no Swagger.

> :bulb: Para ter acesso à documentação e testar os endpoints da aplicação, é necessário que o código esteja em execução na máquina.

Acesse a documentação em formato [JSON](http://localhost:5000/api/carros.json). Ou:

<p align="center"><a href="http://localhost:5000/api/carros.html#!/carros/alugaCarro"><img src="https://img.shields.io/badge/-Run%20in%20Swagger-%2385EA2D?style=flat&logo=swagger&logoColor=black"></a></p>

## 🦸 Autora
<img src="https://avatars3.githubusercontent.com/u/73648823?s=460&u=81cc56a7c802bd21b265dfb0dadadccce01ec987&v=4" height="100" width="100">
Raquel Câmara Porto :maple_leaf:

<a href="https://www.linkedin.com/in/raquel-camara/"><img src="https://img.shields.io/badge/-Raquel-%230077B5?style=flat-square&logo=linkedin&logoColor=white"></a> <a href="mailto:raquelc.porto@outlook.com"><img src="https://img.shields.io/badge/-raquelc.porto@outlook.com-%230078D4?style=flat-square&logo=microsoft-outlook&logoColor=white"></a>
