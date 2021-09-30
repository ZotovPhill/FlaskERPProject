FROM python:3.9.0-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get -y update \
    && apt-get -y install apt-utils build-essential software-properties-common \
      wget git libpq5 libpq-dev libsm6 \
      libxext6 libffi-dev curl\
      libcurl4-openssl-dev libssl-dev\
    && apt-get clean

RUN python -m pip install -U pip
RUN pip install poetry

WORKDIR /usr/src/erp

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

COPY app app
COPY .env entrypoint.sh entrypoint-celery.sh ./
RUN chmod +x entrypoint.sh entrypoint-celery.sh
