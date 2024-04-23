.PHONY: docker push_image

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep -m 1 '^version = ' pyproject.toml | awk -F '"' '{print $$2}')

docker:
	docker build -t ${PROJECT}/usage_service -t ${PROJECT}/usage_service:${VERSION} .

push_image: docker
	docker push ${PROJECT}/usage_service
	docker push ${PROJECT}/usage_service:${VERSION}
