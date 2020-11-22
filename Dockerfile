FROM python:3.8

RUN mkdir /src
WORKDIR /src

RUN apt update && \
    apt install -y postgresql-client

COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
