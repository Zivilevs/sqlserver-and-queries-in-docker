FROM python:3.10-slim-bullseye
#FROM ubuntu:20.04

COPY ./code /var/code

WORKDIR /var/code

RUN apt update && apt install -y curl unixodbc gnupg2
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && apt-get update

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
