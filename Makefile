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

project:
	docker-compose up

projectbuild:
	docker-compose up --build

# Django
run:
	./manage.py runserver

# Poetry

export_plugin:
	poetry self add poetry-plugin-export

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
	flake8

