FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONBUFFEREDWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000