FROM python:3.9

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -qy default-libmysqlclient-dev build-essential netcat

RUN pip install --upgrade pip && pip install -r requirements.txt
