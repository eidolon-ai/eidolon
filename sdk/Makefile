.PHONY: docker push_image maybe_docker_push

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep -m 1 '^version = ' pyproject.toml | awk -F '"' '{print $$2}')

docker:
	docker build --target sdk_base -t ${PROJECT}/sdk_base -t ${PROJECT}/sdk_base:${VERSION} .
	docker build -t ${PROJECT}/sdk -t ${PROJECT}/sdk:${VERSION} .

push_image: docker
	docker push ${PROJECT}/sdk_base
	docker push ${PROJECT}/sdk_base:${VERSION}
	docker push ${PROJECT}/sdk
	docker push ${PROJECT}/sdk:${VERSION}

maybe_docker_push:
	@docker manifest inspect $(PROJECT)/sdk:$(VERSION) >/dev/null && echo "Image exists" || $(MAKE) push_image
