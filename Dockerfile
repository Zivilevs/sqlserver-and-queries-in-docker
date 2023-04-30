FROM python:3.10-slim-bullseye

COPY . 
WORKDIR /var/code

COPY ./code/requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
