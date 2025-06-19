# Docker
network:
	docker network create flix_network
db:
	docker run --name flix_db \
	-e POSTGRES_DB=${PG_NAME} \
	-e POSTGRES_PASSWORD=${PG_PASSWORD} \
	-p ${PG_PORT}:${PG_PORT} \
	-v "/home/willames/TI/Cursos/Django Master/flix-api/.pg_flix:/var/lib/postgresql/data" \
	--network=flix_network \
	-d postgres

destroydb:
	docker stop flix_db
	docker rm flix_db
web:
	docker run  --name flix_web \
	--env-file .env \
	--network=flix_network \
	-p 8000:8000 \
	flix_web:0.1
destroyweb:
	docker stop flix_web
	docker rm flix_web
build:
	docker compose build
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
	docker-compose exec -T flix_web python manage.py test
migrate:
	docker-compose exec -T flix_web python manage.py migrate

makemigrations:
	docker-compose exec -T flix_web python manage.py makemigrations
run:
	docker-compse exec -T

# Poetry
export_plugin:
	poetry self add poetry-plugin-export
poetry-install:
	pip install poetry
poetry-requirements:
	poetry add $(cat requirements.txt)
poetry-dev-requirements:
	poetry add --group-dev $(cat requirements_dev.txt)
requirements:
	poetry export \
	--format=requirements.txt \
	--without-hashes \
	--without group_dev \
	--output=requirements.txt

	sed -i 's/ *;.*//' requirements.txt
requirements_dev:
	poetry export \
	--format=requirements.txt \
	--without-hashes \
	--only group_dev \
	--output=requirements_dev.txt

	sed -i 's/ *;.*//' requirements_dev.txt
# Linter
lint:
	docker-compose exec -T flix_web flake8 .

