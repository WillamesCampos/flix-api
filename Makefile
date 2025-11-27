# Docker Parameters
IMAGE_NAME ?= willamesdev/flix_api
TAG ?= latest
COMPOSE_FILE ?= infrastructure/docker-compose.yml

COMPOSE = docker compose -f $(COMPOSE_FILE)

# =======================================================================

.PHONY: help
help: ## List all available commands
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =============================
# DOCKER
# =============================

up: ## Start all Docker services
	$(COMPOSE) up

up-d: ## Start all Docker services in background
	$(COMPOSE) up -d

up-build: ## Build and start Docker services
	$(COMPOSE) up --build

down: ## Stop and remove Docker services
	$(COMPOSE) down

logs: ## Show Docker services logs
	$(COMPOSE) logs -f

build: ## Build Docker image
	$(COMPOSE) build

build-image: ## Build Docker image for publishing
	docker build -t $(IMAGE_NAME):$(TAG) -t $(IMAGE_NAME):latest -f infrastructure/Dockerfile .

push: ## Publish Docker image to registry
	docker push $(IMAGE_NAME):$(TAG)
	docker push $(IMAGE_NAME):latest

destroy-db: ## Stop and remove database container
	docker stop flix_db || true
	docker rm flix_db || true

destroy-web: ## Stop and remove web application container
	docker stop flix_web || true
	docker rm flix_web || true

dev-db: ## Start only database in background
	$(COMPOSE) up flix_db -d

dev-mongo: ## Start only MongoDB in background
	$(COMPOSE) up mongo -d

dev-celery: ## Start only Celery worker in background
	$(COMPOSE) up celery_worker -d

dev: ## Start development services
	$(COMPOSE) up flix_db mongo celery_worker -d

# =============================
# DJANGO
# =============================

migrate: ## Run Django migrations
	$(COMPOSE) exec -T flix_web python manage.py migrate

makemigrations: ## Create new Django migrations
	$(COMPOSE) exec -T flix_web python manage.py makemigrations

run: ## Start Django development server (Docker)
	$(COMPOSE) exec -T flix_web python manage.py runserver

run-dev: ## Start Django development server (local)
	python manage.py runserver

shell: ## Open Django shell (Docker)
	$(COMPOSE) exec -T flix_web python manage.py shell

shell-dev: ## Open Django shell (local)
	python manage.py shell

# =============================
# TESTING
# =============================

test: ## Run tests and generate coverage report
	python -m pytest -vvv
	coverage html

test-docker: ## Run tests inside Docker container
	$(COMPOSE) exec -T flix_web python -m pytest -vvv

coverage: ## Show coverage report
	coverage report

coverage-html: ## Generate HTML coverage report
	coverage html

# =============================
# LINTING
# =============================

lint: ## Check code with ruff
	ruff check

fix: ## Fix issues found by ruff
	ruff check --fix

format: ## Format code with ruff
	ruff format
