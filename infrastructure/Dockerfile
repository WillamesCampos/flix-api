FROM python:3.13-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install netcat-openbsd to check if the services are ready
# needed for the entrypoint (nc)
RUN apk add --no-cache netcat-openbsd

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry --no-cache-dir
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without group_dev

COPY . .

COPY infrastructure/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
