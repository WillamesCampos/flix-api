FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONBUFFEREDWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

COPY pyproject.toml poetry.lock ./

COPY . .

RUN pip install --upgrade pip
RUN pip install poetry --no-cache-dir
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without group_dev

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
