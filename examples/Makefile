.PHONY: docker_code_search

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep '^version = ' ../sdk/pyproject.toml | awk -F '"' '{print $$2}')

# Define the directories
EIDOLON_SDK_DIR := ../sdk/eidolon_ai_sdk
DOCS_DIR := ../docs

# The target depends on all files in the eidolon_ai_sdk and docs directories
dist/code_search: $(wildcard ${EIDOLON_SDK_DIR}/*) $(wildcard ${DOCS_DIR}/*)
	rm -rf dist/code_search
	mkdir -p dist/code_search/sdk
	cp -r $(EIDOLON_SDK_DIR) dist/code_search/sdk/eidolon_ai_sdk
	cp -r $(DOCS_DIR) dist/code_search/docs

docker_code_search: dist/code_search Dockerfile
	docker build -t ${PROJECT}/code_search -t ${PROJECT}/code_search:${VERSION} -f Dockerfile.code_search .
