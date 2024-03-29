ARG BASE_IMAGE=python:3.11-slim

FROM ${BASE_IMAGE} as builder
RUN pip install poetry
COPY . .
RUN poetry build
RUN poetry export --without-hashes --format=requirements.txt | sed '/@ file/d' > dist/requirements.txt

FROM ${BASE_IMAGE}
COPY --from=builder dist/requirements.txt /tmp/eidolon_ai_sdk/requirements.txt
RUN pip install -r /tmp/eidolon_ai_sdk/requirements.txt
COPY --from=builder dist/*.whl /tmp/eidolon_ai_sdk/
RUN pip install /tmp/eidolon_ai_sdk/*.whl