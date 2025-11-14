# Docker Parameters
IMAGE_NAME ?= willamesdev/flix_api
TAG ?= latest

.PHONY: help
help: ## List all available commands
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =============================
# DOCKER
# =============================

up: ## Start all Docker services
	docker compose up

up-d: ## Start all Docker services in background
	docker compose up -d

up-build: ## Build and start Docker services
	docker compose up --build

down: ## Stop and remove Docker services
	docker compose down

logs: ## Show Docker services logs
	docker compose logs -f

build: ## Build Docker image
	docker compose build

build-image: ## Build Docker image for publishing
	docker build -t $(IMAGE_NAME):$(TAG) -t $(IMAGE_NAME):latest .

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
	docker compose up flix_db -d

dev-mongo: ## Start only MongoDB in background
	docker compose up mongo -d

# =============================
# DJANGO
# =============================

migrate: ## Run Django migrations
	docker compose exec -T flix_web python manage.py migrate

makemigrations: ## Create new Django migrations
	docker compose exec -T flix_web python manage.py makemigrations

run: ## Start Django development server (Docker)
	docker compose exec -T flix_web python manage.py runserver

run-dev: ## Start Django development server (local)
	python manage.py runserver

shell: ## Open Django shell (Docker)
	docker compose exec flix_web python manage.py shell

shell-dev: ## Open Django shell (local)
	python manage.py shell

# =============================
# TESTING
# =============================

test: ## Run tests and generate coverage report
	python -m pytest -vvv
	coverage html

test-docker: ## Run tests inside Docker container
	docker compose exec -T flix_web python -m pytest -vvv

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
