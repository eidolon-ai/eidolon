ARG EIDOLON_VERSION=latest
FROM python:3.11-slim as builder
RUN pip install poetry
COPY . .
RUN mkdir dist
RUN touch dist/requirements.txt
RUN poetry export --without dev --without-hashes --format=requirements.txt | sed '/@ file/d' > dist/requirements.txt

FROM docker.io/eidolonai/sdk:$EIDOLON_VERSION as examples
COPY --from=builder dist/requirements.txt /tmp/examples/requirements.txt
RUN pip install -r /tmp/examples/requirements.txt

ARG LOC=eidolon_examples
FROM examples
WORKDIR /app
COPY $LOC .
