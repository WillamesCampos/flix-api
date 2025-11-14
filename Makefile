# Docker Parameters
IMAGE_NAME ?= willamesdev/flix_api
TAG ?= latest

.PHONY: help
help: ## Lista todos os comandos disponíveis
	@echo "Comandos disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =============================
# DOCKER
# =============================

up: ## Inicia todos os serviços Docker
	docker compose up

up-d: ## Inicia todos os serviços Docker em background
	docker compose up -d

up-build: ## Constrói e inicia os serviços Docker
	docker compose up --build

down: ## Para e remove os serviços Docker
	docker compose down

logs: ## Mostra os logs dos serviços Docker
	docker compose logs -f

build: ## Constrói a imagem Docker
	docker compose build

build-image: ## Constrói a imagem Docker para publicação
	docker build -t $(IMAGE_NAME):$(TAG) -t $(IMAGE_NAME):latest .

push: ## Publica a imagem Docker no registry
	docker push $(IMAGE_NAME):$(TAG)
	docker push $(IMAGE_NAME):latest

destroy-db: ## Para e remove o container do banco de dados
	docker stop flix_db || true
	docker rm flix_db || true

destroy-web: ## Para e remove o container da aplicação web
	docker stop flix_web || true
	docker rm flix_web || true

dev-db: ## Inicia apenas o banco de dados em background
	docker compose up flix_db -d

dev-mongo: ## Inicia apenas o MongoDB em background
	docker compose up mongo -d

# =============================
# DJANGO
# =============================

migrate: ## Executa as migrações do Django
	docker compose exec -T flix_web python manage.py migrate

makemigrations: ## Cria novas migrações do Django
	docker compose exec -T flix_web python manage.py makemigrations

run: ## Inicia o servidor de desenvolvimento Django (Docker)
	docker compose exec -T flix_web python manage.py runserver

run-dev: ## Inicia o servidor de desenvolvimento Django (local)
	python manage.py runserver

shell: ## Abre o shell do Django (Docker)
	docker compose exec flix_web python manage.py shell

shell-dev: ## Abre o shell do Django (local)
	python manage.py shell

# =============================
# TESTING
# =============================

test: ## Executa os testes e gera relatório de coverage
	python -m pytest -vvv
	coverage html

test-docker: ## Executa os testes dentro do container Docker
	docker compose exec -T flix_web python -m pytest -vvv

coverage: ## Mostra o relatório de coverage
	coverage report

coverage-html: ## Gera o relatório de coverage em HTML
	coverage html

# =============================
# LINTING
# =============================

lint: ## Verifica o código com ruff
	ruff check

fix: ## Corrige problemas encontrados pelo ruff
	ruff check --fix

format: ## Formata o código com ruff
	ruff format
