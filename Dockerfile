ARG EIDOS_VERSION=latest
FROM llalor/code-search:$EIDOS_VERSION

ENV PYTHONUNBUFFERED 1

COPY examples/eidolon_examples/code_search/resources /usr/src/code_search/resources
COPY sdk/eidos_sdk /usr/src/sdk/eidos_sdk
COPY docs /usr/src/docs

WORKDIR /usr/src/code_search
CMD exec eidos-server resources -m local_dev
