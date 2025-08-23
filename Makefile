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

# ======================================
# Testing and Development
# ======================================
test:
	make -f Makefile.dev test
devdb:
	make -f Makefile.dev devdb
lint:
	make -f Makefile.dev lint
fix:
	make -f Makefile.dev fix
format:
	make -f Makefile.dev format
coverage:
	make -f Makefile.dev coverage
devrun:
	make -f Makefile.dev run_dev
devrunc:
	make -f Makefile.dev up
devdb:
	make -f Makefile.dev devdb
devlogs:
	make -f Makefile.dev mongo
