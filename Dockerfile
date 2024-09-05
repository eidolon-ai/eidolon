ARG BASE_IMAGE=python:3.11-slim

FROM ${BASE_IMAGE} AS builder_base
RUN pip install poetry

FROM builder_base AS eidolon_client_builder
COPY client/python .
RUN poetry build

FROM builder_base AS usage_client_builder
COPY usage-service/usage-client .
RUN poetry build

FROM builder_base AS builder
COPY sdk .
RUN poetry build
RUN poetry export --without dev --without-hashes --format=requirements.txt | grep -v "eidolon-ai-client" | grep -v "eidolon-ai-usage-client" | grep -v "-e file:///" > dist/requirements.txt
RUN poetry export --without dev -E rag --without-hashes --format=requirements.txt | grep -v "eidolon-ai-client" | grep -v "eidolon-ai-usage-client" | grep -v "-e file:///" > dist/rag.txt
RUN poetry export --without dev -E memory --without-hashes --format=requirements.txt | grep -v "eidolon-ai-client" | grep -v "eidolon-ai-usage-client" | grep -v "-e file:///" > dist/memory.txt
RUN poetry export --without dev -E sql --without-hashes --format=requirements.txt | grep -v "eidolon-ai-client" | grep -v "eidolon-ai-usage-client" | grep -v "-e file:///" > dist/sql.txt
RUN poetry export --without dev -E file --without-hashes --format=requirements.txt | grep -v "eidolon-ai-client" | grep -v "eidolon-ai-usage-client" | grep -v "-e file:///" > dist/file.txt

FROM ${BASE_IMAGE} AS sdk_base

COPY --from=builder dist/requirements.txt /tmp/eidolon_ai_sdk/requirements.txt
RUN pip install -r /tmp/eidolon_ai_sdk/requirements.txt --no-cache --no-deps

COPY --from=builder dist/rag.txt /tmp/eidolon_ai_sdk/rag.txt
RUN pip install -r /tmp/eidolon_ai_sdk/rag.txt --no-cache --no-deps

COPY --from=builder dist/memory.txt /tmp/eidolon_ai_sdk/memory.txt
RUN pip install -r /tmp/eidolon_ai_sdk/memory.txt --no-cache --no-deps

COPY --from=builder dist/sql.txt /tmp/eidolon_ai_sdk/sql.txt
RUN pip install -r /tmp/eidolon_ai_sdk/sql.txt --no-cache --no-deps

COPY --from=builder dist/file.txt /tmp/eidolon_ai_sdk/file.txt
RUN pip install -r /tmp/eidolon_ai_sdk/file.txt --no-cache --no-deps

COPY --from=eidolon_client_builder dist/*.whl /tmp/eidolon_ai_client/
RUN pip install /tmp/eidolon_ai_client/*.whl --no-cache --no-deps
COPY --from=usage_client_builder dist/*.whl /tmp/usage_client/
RUN pip install /tmp/usage_client/*.whl --no-cache --no-deps
COPY --from=builder dist/*.whl /tmp/eidolon_ai_sdk/
RUN pip install /tmp/eidolon_ai_sdk/*.whl --no-cache --no-deps

RUN pip install chromadb-client --no-cache --no-deps

FROM sdk_base AS runner
RUN addgroup --system --gid 1001 eidolon
RUN adduser --system --uid 1001 eidolon
RUN chmod 755 /usr/local/bin/eidolon-server
USER eidolon
EXPOSE 8080
ENV PYTHONUNBUFFERED 1
WORKDIR app
ENTRYPOINT ["eidolon-server"]
CMD ["resources"]
