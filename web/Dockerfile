FROM python:3.9-slim

RUN pip install poetry

RUN mkdir /app
WORKDIR /app
COPY poetry.lock pyproject.toml main.py /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

