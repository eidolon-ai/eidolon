.PHONY: docker push_image

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep '^version = ' pyproject.toml | awk -F '"' '{print $$2}')

.make_poetry_install: pyproject.toml poetry.lock
	poetry install
	@touch $@

dist: .make_poetry_install $(wildcard eidolon_ai_sdk/*)
	rm -f dist/eidolon_ai_sdk*.tar.gz.
	rm -f dist/eidolon_ai_sdk*.whl.
	poetry build

dist/requirements.txt: poetry.lock pyproject.toml
	poetry export --without-hashes --format=requirements.txt > dist/requirements.txt

docker:  dist dist/requirements.txt Dockerfile
	docker build -t ${PROJECT}/sdk -t ${PROJECT}/sdk:${VERSION} .

push_image: docker
	docker push ${PROJECT}/sdk
	docker push ${PROJECT}/sdk:${VERSION}
