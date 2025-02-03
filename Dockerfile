FROM python:3.13-alpine
MAINTAINER Sonya Karmeeva

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi && \
    apk del .tmp-build-deps

COPY src /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D sonya
RUN chown -R sonya:sonya /vol/  # Меняем владельца директории
RUN chmod -R 755 /vol/web  # Даем права на запись в директорию
USER sonya