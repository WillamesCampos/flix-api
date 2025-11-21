<div align="center">
  <img width="250" height="250" alt="Flix API Logo" src="https://github.com/user-attachments/assets/440f8f65-1f9e-4a9a-98e7-1cfd1a73f8e6" />
</div>

# 🎬 Flix API

> **🇺🇸 English Version Available**: [README.md](README.md)

API RESTful desenvolvida com Django e Django REST Framework para gerenciamento de filmes, atores, gêneros e avaliações. O projeto foi desenvolvido seguindo as melhores práticas de desenvolvimento Django, com arquitetura modular, testes abrangentes e CI/CD configurado.

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Uso](#-uso)
- [Comandos Makefile](#-comandos-makefile)
- [Testes](#-testes)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Deploy](#-deploy)
- [Desafios e Soluções](#-desafios-e-soluções)
- [Contribuindo](#-contribuindo)

## 🎯 Sobre o Projeto

Flix API é uma aplicação backend completa para gerenciamento de um catálogo de filmes. O projeto foi desenvolvido como parte do aprendizado de desenvolvimento de APIs com Django REST Framework, implementando conceitos avançados como:

- Autenticação JWT
- Permissões customizadas baseadas em modelos
- Serializers com validações complexas
- Testes automatizados com alta cobertura
- Migrações de banco de dados complexas
- Arquitetura baseada em serviços
- Integração com múltiplos bancos de dados (PostgreSQL e MongoDB)

## 🚀 Funcionalidades

### CRUD Completo
- ✅ **Movies (Filmes)**: Gerenciamento completo de filmes com relacionamentos com atores e gêneros
- ✅ **Actors (Atores)**: CRUD de atores com informações de nacionalidade e data de nascimento
- ✅ **Genres (Gêneros)**: Gerenciamento de categorias de filmes
- ✅ **Reviews (Avaliações)**: Sistema de avaliações com notas e comentários

### Funcionalidades Especiais
- 📊 **Estatísticas de Filmes**: Endpoint dedicado para estatísticas agregadas
- 📥 **Importação via CSV**: Comandos Django para importar atores e filmes via arquivos CSV
  - Veja [Formato CSV de Atores](instructions/import_csv/actors.md)
  - Veja [Formato CSV de Filmes](instructions/import_csv/movies.md)
- 🔐 **Autenticação JWT**: Sistema completo de autenticação com tokens
- 🛡️ **Sistema de Permissões**: Permissões granulares baseadas em modelos e ações

## 🧰 Tecnologias

### Backend
- **Python 3.13**
- **Django 5.2.1** - Framework web
- **Django REST Framework 3.16.0** - Framework para APIs REST
- **Django REST Framework Simple JWT 5.5.0** - Autenticação JWT

### Banco de Dados
- **PostgreSQL** - Banco de dados relacional principal
- **MongoDB** - Banco de dados NoSQL (para logs e dados não relacionais)

### Ferramentas de Desenvolvimento
- **Poetry** - Gerenciamento de dependências
- **Pytest** - Framework de testes
- **Ruff** - Linter e formatação de código
- **Factory Boy** - Criação de fixtures para testes
- **Coverage** - Análise de cobertura de testes

### DevOps
- **Docker** - Containerização da aplicação
- **Docker Compose** - Orquestração de containers
- **GitHub Actions** - CI/CD

## 📦 Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:

- **Python 3.11+**
- **Poetry** ([Instalação](https://python-poetry.org/docs/#installation))
- **Docker** e **Docker Compose** ([Instalação](https://docs.docker.com/get-docker/))
- **Git**

## 🔧 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/WillamesCampos/flix-api.git
cd flix-api
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Django
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DEBUG=DEV
ALLOWED_HOSTS=*

# PostgreSQL
POSTGRES_DB=flix_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua-senha-postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# MongoDB
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=sua-senha-mongo
MONGO_INITDB_DATABASE=flix_logs
MONGO_URI=mongodb://root:sua-senha-mongo@mongo:27017/flix_logs?authSource=admin
```

### 3. Instale as dependências

```bash
poetry install
```

### 4. Execute com Docker (Recomendado)

```bash
# Construir e iniciar os containers
make up-build

# Ou iniciar em background
make up-d

# Executar migrações
make migrate
```

### 5. Ou execute localmente

```bash
# Inicie apenas o banco de dados
make dev-db
make dev-mongo

# Execute as migrações
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser

# Inicie o servidor
make run-dev
```

A API estará disponível em `http://localhost:8000`

## 📖 Uso

### Autenticação

Primeiro, obtenha um token JWT:

```bash
curl -X POST http://localhost:8000/api/v1/authentication/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu-usuario",
    "password": "sua-senha"
  }'
```

Use o token retornado nas requisições subsequentes:

```bash
curl -X GET http://localhost:8000/api/v1/movies/ \
  -H "Authorization: Bearer seu-token-aqui"
```

### Endpoints Principais

#### Movies
- `GET /api/v1/movies/` - Lista todos os filmes
- `POST /api/v1/movies/` - Cria um novo filme
- `GET /api/v1/movies/{uuid}/` - Detalhes de um filme
- `PATCH /api/v1/movies/{uuid}/` - Atualiza um filme
- `DELETE /api/v1/movies/{uuid}/` - Remove um filme
- `GET /api/v1/movies/stats/` - Estatísticas dos filmes

#### Actors
- `GET /api/v1/actors/` - Lista todos os atores
- `POST /api/v1/actors/` - Cria um novo ator
- `GET /api/v1/actors/{uuid}/` - Detalhes de um ator
- `PATCH /api/v1/actors/{uuid}/` - Atualiza um ator
- `DELETE /api/v1/actors/{uuid}/` - Remove um ator

#### Genres
- `GET /api/v1/genres/` - Lista todos os gêneros
- `POST /api/v1/genres/` - Cria um novo gênero
- `GET /api/v1/genres/{uuid}/` - Detalhes de um gênero
- `PATCH /api/v1/genres/{uuid}/` - Atualiza um gênero
- `DELETE /api/v1/genres/{uuid}/` - Remove um gênero

#### Reviews
- `GET /api/v1/reviews/` - Lista todas as avaliações
- `POST /api/v1/reviews/` - Cria uma nova avaliação
- `GET /api/v1/reviews/{uuid}/` - Detalhes de uma avaliação
- `PATCH /api/v1/reviews/{uuid}/` - Atualiza uma avaliação
- `DELETE /api/v1/reviews/{uuid}/` - Remove uma avaliação

### Comandos de Importação CSV

#### Importar Atores

```bash
python manage.py import_actors caminho/para/arquivo.csv
```

Para o formato do arquivo CSV, veja [instructions/import_csv/actors.md](instructions/import_csv/actors.md)

#### Importar Filmes

```bash
python manage.py import_movies caminho/para/arquivo.csv
```

Para o formato do arquivo CSV, veja [instructions/import_csv/movies.md](instructions/import_csv/movies.md)

## 🛠️ Comandos Makefile

O projeto possui um Makefile completo para facilitar o desenvolvimento. Execute `make help` para ver todos os comandos disponíveis.

### Docker

```bash
make up              # Inicia todos os serviços Docker
make up-d            # Inicia todos os serviços Docker em background
make up-build         # Constrói e inicia os serviços Docker
make down             # Para e remove os serviços Docker
make logs             # Mostra os logs dos serviços Docker
make build            # Constrói a imagem Docker
make build-image      # Constrói a imagem Docker para publicação
make push             # Publica a imagem Docker no registry
make dev-db           # Inicia apenas o banco de dados em background
make dev-mongo        # Inicia apenas o MongoDB em background
make destroy-db       # Para e remove o container do banco de dados
make destroy-web      # Para e remove o container da aplicação web
```

### Django

```bash
make migrate          # Executa as migrações do Django (Docker)
make makemigrations   # Cria novas migrações do Django (Docker)
make run              # Inicia o servidor de desenvolvimento Django (Docker)
make run-dev          # Inicia o servidor de desenvolvimento Django (local)
make shell            # Abre o shell do Django (Docker)
make shell-dev        # Abre o shell do Django (local)
```

### Testes

```bash
make test             # Executa os testes e gera relatório de coverage
make test-docker      # Executa os testes dentro do container Docker
make coverage         # Mostra o relatório de coverage
make coverage-html    # Gera o relatório de coverage em HTML
```

### Linting e Formatação

```bash
make lint             # Verifica o código com ruff
make fix              # Corrige problemas encontrados pelo ruff
make format           # Formata o código com ruff
```

## 🧪 Testes

O projeto possui uma suíte completa de testes com alta cobertura de código.

### Executar Testes

```bash
# Executar todos os testes
make test

# Executar testes com mais verbosidade
pytest -vvv

# Executar testes de um app específico
pytest movies/tests/

# Executar um teste específico
pytest movies/tests/test_views.py::TestMoviesAPI::test_create_movie_success
```

### Cobertura de Código

O projeto mantém uma cobertura mínima de 75%. Para ver o relatório:

```bash
make coverage        # Relatório no terminal
make coverage-html   # Relatório HTML em htmlcov/
```

## 📂 Estrutura do Projeto

```
flix-api/
├── actors/              # App de Atores
│   ├── management/      # Comandos Django customizados
│   ├── migrations/      # Migrações do banco de dados
│   ├── tests/          # Testes do app
│   ├── models.py       # Modelos de dados
│   ├── serializers.py  # Serializers da API
│   ├── views.py        # Views da API
│   └── urls.py         # Rotas do app
├── genres/             # App de Gêneros
├── movies/              # App de Filmes
│   └── services/        # Serviços de negócio
├── reviews/            # App de Avaliações
├── authentication/     # Autenticação JWT
├── core/               # Modelos base compartilhados
├── app/                # Configurações principais
│   ├── settings.py     # Configurações do Django
│   ├── permissions.py  # Permissões customizadas
│   └── urls.py         # URLs principais
├── logs/               # Sistema de logs
├── conftest.py         # Configurações do pytest
├── docker-compose.yml  # Configuração Docker Compose
├── Dockerfile          # Imagem Docker
├── Makefile           # Comandos automatizados
├── pyproject.toml     # Configurações Poetry
└── README.md          # Este arquivo
```

### Arquitetura

O projeto segue uma arquitetura modular onde cada app Django é responsável por um domínio específico:

- **Separação de responsabilidades**: Cada app tem sua própria lógica de negócio
- **Modelos base**: Uso de `BaseModel` para campos comuns (UUID, timestamps, auditoria)
- **Serviços**: Lógica de negócio complexa isolada em classes de serviço
- **Permissões**: Sistema de permissões centralizado e reutilizável

## 🚀 Deploy

### Docker Hub

O projeto está configurado para publicação automática no Docker Hub através do GitHub Actions.

```bash
# Construir imagem para produção
make build-image TAG=v1.0.0

# Publicar no Docker Hub
make push TAG=v1.0.0
```

### GitHub Actions

O projeto possui workflows configurados para:

- **Quality Assurance**: Executa lint e testes em Pull Requests
- **Docker Image Release**: Publica imagens Docker quando tags são criadas
- **Publish**: Pipeline completo de validação e publicação

### Variáveis de Ambiente para Produção

Certifique-se de configurar as seguintes variáveis no ambiente de produção:

```env
DEBUG=False
DJANGO_SECRET_KEY=chave-secreta-forte
ALLOWED_HOSTS=seu-dominio.com
# ... outras variáveis
```

## 🎓 Desafios e Soluções

### 1. Migração de ID para UUID como Primary Key

**Desafio**: Migrar todos os modelos de `id` (BigAutoField) para `uuid` (UUIDField) como chave primária, mantendo a integridade dos dados e relacionamentos.

**Solução**:
- Criação de migrações sequenciais que removem o campo `id` e adicionam `uuid`
- Implementação de `BaseModel` com UUID como PK padrão
- Migração especial para tabela intermediária ManyToMany (`movies_movie_actors`)
- Atualização de todos os testes e serializers para usar `uuid` em vez de `id`

**Lições Aprendidas**:
- Em produção, seria necessário criar uma tabela de mapeamento manual
- Abordagem mais segura: criar UUID como campo único primeiro, depois migrar gradualmente
- Sempre fazer backup antes de migrações estruturais complexas

### 2. Tabela Intermediária ManyToMany

**Desafio**: A tabela intermediária `movies_movie_actors` mantinha referências `bigint` enquanto os modelos usavam UUID.

**Solução**:
- Criação de migração que remove constraints antigas
- Limpeza da tabela (em desenvolvimento)
- Recriação das colunas com tipo UUID
- Recriação de todas as constraints e foreign keys

### 3. Sistema de Permissões Customizado

**Desafio**: Implementar um sistema de permissões granular baseado em modelos e ações.

**Solução**:
- Criação de `GlobalDefaultPermission` que verifica permissões Django padrão
- Integração com sistema de grupos e permissões do Django
- Reutilização em todas as views através de `permission_classes`

### 4. Testes com Alta Cobertura

**Desafio**: Manter cobertura de testes acima de 75% com testes significativos.

**Solução**:
- Uso de `Factory Boy` para criar fixtures de teste
- Criação de `BaseAPITest` para testes de API reutilizáveis
- Testes unitários para modelos, serializers e serviços
- Testes de integração para views e endpoints

### 5. CI/CD com GitHub Actions

**Desafio**: Configurar pipeline completo de CI/CD com testes, lint e publicação de imagens.

**Solução**:
- Workflows separados para QA e publicação
- Execução de testes em ambiente isolado com PostgreSQL
- Publicação automática de imagens Docker no Docker Hub
- Validação de qualidade antes de publicação

### 6. Tarefas Assíncronas com Celery e Redis

**Desafio**: Implementar notificações por email quando avaliações são criadas sem bloquear a resposta da API.

**Solução**:
- **Celery** para execução assíncrona de tarefas
- **Redis** como message broker entre Django e workers do Celery
- **Django Signals** para disparar tarefas automaticamente quando avaliações são criadas
- Containers Docker separados para aplicação web e worker do Celery

**Lições Aprendidas**:

**Configuração do Celery**:
- O Celery deve ser inicializado em `app/celery.py` e importado em `app/__init__.py` para garantir que carregue com o Django
- Use o decorador `@shared_task` para tarefas que podem ser reutilizadas entre apps
- Configure as settings do Celery no Django settings com prefixo `CELERY_`
- Use `CELERY_BROKER_URL` e `CELERY_RESULT_BACKEND` apontando para Redis

**Redis como Message Broker**:
- Redis atua como uma fila: Django coloca tarefas, workers do Celery pegam
- Rápido e confiável para enfileiramento de tarefas
- Use o nome do serviço no Docker Compose (`redis://redis:6379/0`) em vez de `localhost`

**Integração com Django Signals**:
- Signals permitem ações automáticas quando modelos são salvos
- Use `@receiver(post_save, sender=Model)` para escutar eventos do modelo
- Sempre envolva handlers de signals em try-except para evitar que erros quebrem a requisição principal
- Registre signals em `apps.py` com método `ready()` para garantir que carreguem

**Docker Compose para Múltiplos Serviços**:
- Dockerfiles separados para serviços diferentes (web vs worker) otimizam builds
- Use `depends_on` para garantir que serviços iniciem na ordem correta
- Compartilhe variáveis de ambiente mas configure as específicas de cada serviço
- Use scripts de entrypoint para aguardar dependências (Postgres, Redis) antes de iniciar

**Boas Práticas**:
- Sempre passe dados serializáveis para tarefas Celery (UUIDs como strings, não objetos)
- Use `task.delay()` para execução assíncrona, `task.apply_async()` para opções avançadas
- Registre execução e erros de tarefas para debugging
- Teste Celery localmente com `--pool=solo` para debugging

### 7. Orquestração com Docker Compose

**Desafio**: Coordenar múltiplos serviços (Django, PostgreSQL, MongoDB, Redis, Celery) com dependências corretas e ordem de inicialização.

**Solução**:
- Use Docker Compose para definir todos os serviços em um arquivo
- Implemente health checks para bancos de dados
- Crie scripts de entrypoint que aguardam dependências
- Use volumes nomeados para persistência de dados

**Lições Aprendidas**:

**Dependências entre Serviços**:
- `depends_on` garante que serviços iniciem na ordem, mas não espera que estejam prontos
- Use scripts de entrypoint com `nc` (netcat) para verificar se serviços estão realmente prontos
- Health checks ajudam o Docker a saber quando serviços estão operacionais

**Variáveis de Ambiente**:
- Use arquivo `.env` para secrets (nunca commite)
- Passe variáveis de ambiente através do `docker-compose.yml`
- Use nomes de serviços para comunicação entre serviços (`flix_db`, `redis`, não `localhost`)

**Scripts de Entrypoint**:
- Scripts de entrypoint rodam antes do comando principal
- Use-os para rodar migrações, aguardar dependências ou configurar o ambiente
- Sempre use `exec` para o comando final para garantir tratamento adequado de sinais
- Copie scripts de entrypoint DEPOIS de `COPY . .` para preservar permissões

**Gerenciamento de Volumes**:
- Volumes nomeados persistem dados mesmo se containers forem removidos
- Use volumes para bancos de dados para evitar perda de dados
- Volumes diferentes para serviços diferentes previnem conflitos

**Logging**:
- Suprima logs de serviços de infraestrutura (bancos de dados) usando `logging: driver: "none"`
- Mantenha logs da aplicação visíveis para debugging
- Use `docker compose logs -f nome_servico` para seguir logs de serviços específicos

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- Siga o estilo de código definido pelo Ruff
- Execute `make lint` e `make format` antes de commitar
- Mantenha a cobertura de testes acima de 75%
- Escreva testes para novas funcionalidades

## 👤 Autor

**Willames Campos**

- GitHub: [@WillamesCampos](https://github.com/WillamesCampos)
- Email: willwjccampos@gmail.com

## 🙏 Agradecimentos

- Django e Django REST Framework pela excelente documentação
- Comunidade Python/Django pelo suporte
- Todos os mantenedores das bibliotecas open-source utilizadas

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
