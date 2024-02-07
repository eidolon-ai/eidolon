ARG BASE_IMAGE=python:3.11-slim
FROM ${BASE_IMAGE}

# Local caching of pip packages. Does not save full build time, but could be split up if desired.
COPY dist/requirements.txt /tmp/eidolon_ai_sdk/requirements.txt
RUN pip install -r /tmp/eidolon_ai_sdk/requirements.txt

# Copy the wheel file and install it. Should only install eidolon_ai_sdk since remote dependencies are already installed.
COPY dist/*.whl /tmp/eidolon_ai_sdk/
RUN pip install /tmp/eidolon_ai_sdk/*.whl
