ARG BASE_IMAGE=python:3.11-slim

FROM ${BASE_IMAGE} AS builder
RUN pip install poetry
COPY . .
RUN poetry build
RUN poetry export --without-hashes --format=requirements.txt | sed '/@ file/d' > dist/requirements.txt

FROM ${BASE_IMAGE} AS sdk_base
COPY --from=builder dist/requirements.txt /tmp/app/requirements.txt
RUN pip install -r /tmp/app/requirements.txt
COPY --from=builder dist/*.whl /tmp/app/
RUN pip install /tmp/app/*.whl

FROM sdk_base AS runner
RUN addgroup --system --gid 1001 eidolon
RUN adduser --system --uid 1001 eidolon
USER eidolon
EXPOSE 8080
ENV PYTHONUNBUFFERED 1
WORKDIR app
ENTRYPOINT ["usage-service"]