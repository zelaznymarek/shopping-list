FROM python:3.8.1

COPY requirements.txt /requirements.txt
COPY app/ app/

RUN pip install -r requirements.txt

WORKDIR app/

CMD python app.py
