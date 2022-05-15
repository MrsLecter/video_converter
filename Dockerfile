# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip install psycopg2-binary

COPY . .

ENV FLASK_APP=main.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]