# Docker Parameters
IMAGE_NAME ?= willamescampos/flix_api
TAG ?= latest

# Docker
destroydb:
	docker stop flix_db
	docker rm flix_db

destroyweb:
	docker stop flix_web
	docker rm flix_web

build_web:
	docker build -t $(IMAGE_NAME):$(TAG) -t $(IMAGE_NAME):latest .
up:
	docker compose up -d
down:
	docker compose down
logs:
	docker compose logs -f

projectbuild:
	docker-compose up --build

# Django
test:
	docker compose exec -T flix_web python manage.py test
migrate:
	docker compose exec -T flix_web python manage.py migrate
makemigrations:
	docker compose exec -T flix_web python manage.py makemigrations
run:
	docker compose exec -T flix_web python manage.py runserver


