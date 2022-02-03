FROM python:3.9.7 AS base
FROM base AS builder

WORKDIR /build

ENV HOME /root
ENV PATH ${HOME}/.local/bin:${PATH}

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_VERSION=1.2.0a2 python -

COPY poetry.lock pyproject.toml ./

RUN poetry export --output requirements.txt

WORKDIR /dist

RUN cp /build/requirements.txt ./

COPY app/ ./app/
COPY alembic.ini ./

FROM base AS release

WORKDIR /release

ENV PATH="/release/.venv/bin:$PATH"
ENV PYTHONPATH="/release"

RUN python -m venv /release/.venv

RUN pip install gunicorn

COPY --from=builder /dist/requirements.txt ./

RUN pip install -r requirements.txt

COPY --from=builder /dist/ ./
