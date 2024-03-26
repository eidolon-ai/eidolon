ARG EIDOLON_VERSION=latest
ARG LOC=eidolon_examples

FROM python:3.11-slim as builder
RUN pip install poetry
COPY . .
RUN poetry export --without-hashes --format=requirements.txt > dist/requirements.txt

FROM docker.io/eidolonai/sdk:$EIDOLON_VERSION as examples
COPY --from=builder dist/requirements.txt /tmp/examples/requirements.txt
RUN pip install -r /tmp/examples/requirements.txt

FROM examples
COPY $LOC .
