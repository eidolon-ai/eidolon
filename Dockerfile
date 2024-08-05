ARG BASE_IMAGE=python:3.11-slim

FROM ${BASE_IMAGE} as builder_base
RUN pip install poetry

FROM builder_base as eidolon_client_builder
COPY client/python .
RUN poetry build

FROM builder_base as usage_client_builder
COPY usage-service/usage-client .
RUN poetry build

FROM builder_base as builder
COPY sdk .
RUN poetry build
RUN poetry export --without dev --without-hashes --format=requirements.txt | grep -v "eidolon-ai-client" | grep -v "eidolon-ai-usage-client" | grep -v "-e file:///" > dist/requirements.txt

FROM ${BASE_IMAGE} as sdk_base
COPY --from=builder dist/requirements.txt /tmp/eidolon_ai_sdk/requirements.txt
RUN pip install -r /tmp/eidolon_ai_sdk/requirements.txt
RUN playwright install

COPY --from=eidolon_client_builder dist/*.whl /tmp/eidolon_ai_client/
RUN pip install /tmp/eidolon_ai_client/*.whl
COPY --from=usage_client_builder dist/*.whl /tmp/usage_client/
RUN pip install /tmp/usage_client/*.whl
COPY --from=builder dist/*.whl /tmp/eidolon_ai_sdk/
RUN pip install /tmp/eidolon_ai_sdk/*.whl

FROM sdk_base as runner
RUN addgroup --system --gid 1001 eidolon
RUN adduser --system --uid 1001 eidolon
RUN chmod 755 /usr/local/bin/eidolon-server
USER eidolon
EXPOSE 8080
ENV PYTHONUNBUFFERED 1
WORKDIR app
ENTRYPOINT ["eidolon-server"]
CMD ["resources"]
