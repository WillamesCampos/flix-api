# Flix - API

API Restful para consulta e cadastro de filmes, com o intuito de utilizar de forma eficiente e com boas práticas para projetos Django com Django Rest Framework.


## 🚀 Features

- CRUD de Movies
- CRUD de Actors
- CRUD de Reviews
- CRUD de Genres
- Django Management Command para import de Actors via arquivo `.csv`
- Endpoint com estatísticas dos Movies

## 🧰 Tech Stack

| Área | Tecnologia |
|--------|------------|
| Backend | Django, Django Rest Framework |
| Banco de Dados | PostgreSQL |
| Tarefas Assíncronas | A definir |
| Comunicação em tempo real | A definir |
| Integração AI | A definir |
| Autenticação | Django Rest Simple JWT |
| DevOps | Docker |
| Arquitetura | Projeto Django com boas práticas |

## 📂 Estrutura do Projeto

Este projeto segue boas práticas de um projeto desenvolvido com Django e Django Rest Framework, com o objetivo de separar lógica de negócio e recursos do framework, fazendo alterações mínimas da organização padrão do Django.

A estrutura deste projeto será atualizado à medida que ele evolui.

Os apps do Django são:

- actors
- genres
- movies
- reviews

A pasta authentication contém apenas as views e rotas de gerenciamento de autenticação para gerar e atualizar tokens.

Todas as rotas são precedidas de `/api/v1/nome_do_app/`

Este projeto foi desenvolvido com Sistema Operacional Linux Mint com a versão do python 3.11.0


## Instalação


## Comandos Pré-Definidos do Makefile


## Testes

