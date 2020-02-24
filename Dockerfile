FROM python:3.8.1

WORKDIR /src

COPY .env .env
COPY requirements.txt requirements.txt
COPY config.py config.py

RUN pip install -r requirements.txt

CMD flask run -h 0.0.0.0
