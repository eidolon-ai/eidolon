.PHONY: docker push_image

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep '^version = ' pyproject.toml | awk -F '"' '{print $$2}')

docker:
	docker build -t ${PROJECT}/sdk -t ${PROJECT}/sdk:${VERSION} .

push_image: docker
	docker push ${PROJECT}/sdk
	docker push ${PROJECT}/sdk:${VERSION}
