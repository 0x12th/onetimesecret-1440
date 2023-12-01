FROM python:3.11-slim-buster AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /ots

COPY pyproject.toml pdm.lock /ots/
COPY src/ /ots/src
COPY alembic/ /ots/alembic
COPY alembic.ini /ots/
COPY scripts/ /ots/scripts/

RUN mkdir __pypackages__ && pdm sync --prod --no-editable

FROM python:3.11-slim-buster

ENV PYTHONPATH=/ots/pkgs
COPY --from=builder /ots/__pypackages__/3.11/lib /ots/pkgs

COPY --from=builder /ots/__pypackages__/3.11/bin/* /bin/
COPY --from=builder /ots/src/ /ots/src
COPY --from=builder /ots/alembic/ /ots/alembic
COPY --from=builder /ots/alembic.ini /ots/alembic.ini
COPY --from=builder /ots/scripts/ /ots/scripts

WORKDIR /ots

RUN chmod a+x ./scripts/*.sh
