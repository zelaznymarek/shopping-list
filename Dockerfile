FROM python:3.8.1

COPY app/ app/

WORKDIR app

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY .env /.env

CMD flask run
