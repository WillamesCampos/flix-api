# Docker Parameters
IMAGE_NAME ?= willamesdev/flix_api
TAG ?= latest

# =============================
# Docker Management
# =============================
destroydb:
	docker stop flix_db
	docker rm flix_db
destroyweb:
	docker stop flix_web
	docker rm flix_web
up:
	docker compose up
up_build:
	docker-compose up --build
down:
	docker compose down
logs:
	docker compose logs -f
build:
	docker build -t $(IMAGE_NAME):$(TAG) -t $(IMAGE_NAME):latest .
push:
	docker push $(IMAGE_NAME):$(TAG)
	docker push $(IMAGE_NAME):latest


# =============================
# Django Management
# =============================
migrate:
	docker compose exec -T flix_web python manage.py migrate
makemigrations:
	docker compose exec -T flix_web python manage.py makemigrations
run:
	docker compose exec -T flix_web python manage.py runserver


