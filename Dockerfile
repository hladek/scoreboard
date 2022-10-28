# https://docs.docker.com/samples/django/
# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
WORKDIR /code/scoreboard
# Configuring the app - these have to be changed in production!!!
ENV SECRET_KEY qqqqq
ENV DATABASE_URL sqlite:///db.sqlite3
ENV DEBUG False
CMD daphne -p 8000 -b 0.0.0.0 scoreboard.asgi:application

