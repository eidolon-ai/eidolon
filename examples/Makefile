.PHONY: docker_code_search

PROJECT ?= docker.io/eidosai
VERSION := $(shell grep '^version = ' ../sdk/pyproject.toml | awk -F '"' '{print $$2}')

# Define the directories
EIDOS_SDK_DIR := ../sdk/eidos_sdk
DOCS_DIR := ../docs

# Find all files in the eidos_sdk and docs directories
EIDOS_SDK_FILES := $(shell find $(EIDOS_SDK_DIR) -type f)
DOCS_FILES := $(shell find $(DOCS_DIR) -type f)

# The target depends on all files in the eidos_sdk and docs directories
dist/code_search: $(wildcard ${EIDOS_SDK_DIR}/*) $(wildcard ${DOCS_DIR}/*)
	rm -rf dist/code_search
	mkdir -p dist/code_search/sdk
	cp -r $(EIDOS_SDK_DIR) dist/code_search/sdk/eidos_sdk
	cp -r $(DOCS_DIR) dist/code_search/docs

docker_code_search: dist/code_search Dockerfile.code_search
	docker build -t ${PROJECT}/code_search -t ${PROJECT}/code_search:${VERSION} -f Dockerfile.code_search .
