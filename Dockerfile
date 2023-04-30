FROM python:3.10-slim-bullseye

COPY ./code /var/code

WORKDIR /var/code

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
