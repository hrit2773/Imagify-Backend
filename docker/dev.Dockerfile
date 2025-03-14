FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -m celeryuser

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /imagify

COPY ../requirements.txt /imagify/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /imagify/

USER celeryuser

