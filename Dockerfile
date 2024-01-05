FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED 1

RUN pip install poetry
WORKDIR /usr/src
COPY docs docs
COPY examples examples
COPY sdk sdk
WORKDIR examples
# we could speed up build times by copying the toml/lock first installing so code changes do not invalidate cache
RUN poetry install --no-dev

# perf is going to suck for the first request since we need to load files into agents. We could consider pre-prompting loading some of this
CMD exec poetry run eidos-server eidolon_examples/code_search/resources -m local_dev
