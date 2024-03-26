ARG BASE_IMAGE=python:3.11-slim
FROM ${BASE_IMAGE} as base

FROM python:3.11-slim as builder
RUN pip install poetry
COPY . .
RUN poetry build
RUN poetry export --without-hashes --format=requirements.txt > dist/requirements.txt

FROM base as installer
COPY --from=builder dist/requirements.txt /tmp/eidolon_ai_sdk/requirements.txt
RUN pip install -r /tmp/eidolon_ai_sdk/requirements.txt
COPY --from=builder dist/*.whl /tmp/eidolon_ai_sdk/
RUN pip install /tmp/eidolon_ai_sdk/*.whl
# leaving the two files adds ~300kb to file size but improves cachability of runtime image of copying the venv to seporate runner

FROM installer as runner
RUN addgroup --system --gid 1001 eidolon
RUN adduser --system --uid 1001 eidolon
USER eidolon
EXPOSE 8080
ENV PYTHONUNBUFFERED 1
# todo: we expect resources to be mounted somewhere, mount/resources;
# todo: we likely want to add "mount" to the python path so that we can also add python custmization there as well
WORKDIR app
CMD eidolon-server resources