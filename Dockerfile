FROM python:3.11-slim-buster

ENV PROJECT_DIR=/app
WORKDIR $PROJECT_DIR

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY src/project/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src src
WORKDIR $PROJECT_DIR/src
