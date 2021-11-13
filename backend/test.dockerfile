FROM python:3.9.7

WORKDIR /src

ENV PATH /root/.local/bin:${PATH}

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_VERSION=1.2.0a2 python -

COPY app/ app
COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY alembic.ini ./

COPY tests/ tests
