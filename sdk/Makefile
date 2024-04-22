.PHONY: docker push_image

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep '^version = ' pyproject.toml | awk -F '"' '{print $$2}')

docker:
	docker build --target sdk_base -t ${PROJECT}/sdk_base -t ${PROJECT}/sdk_base:${VERSION} .
	docker build -t ${PROJECT}/sdk -t ${PROJECT}/sdk:${VERSION} .

push_image: docker
	docker push ${PROJECT}/sdk_base
	docker push ${PROJECT}/sdk_base:${VERSION}
	docker push ${PROJECT}/sdk
	docker push ${PROJECT}/sdk:${VERSION}

pyproject.toml: $(wildcard eidolon_ai_sdk/*)
	poetry add eidolon-ai-client@latest
	poetry add eidolon-ai-usage-client@latest
	poetry add eidolon-ai-client@latest
	poetry version patch

