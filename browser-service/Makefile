.PHONY: docker dockerx maybe_docker_push

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep -m 1 '^version = ' pyproject.toml | awk -F '"' '{print $$2}')

poetry.lock: pyproject.toml
	poetry lock --no-update

docker: poetry.lock
	docker build -t browser_service -t ${PROJECT}/browser_service -t ${PROJECT}/browser_service:${VERSION} .

PLATFORMS ?= linux/arm64,linux/amd64
CONTAINER_TOOL ?= docker

dockerx:
	# copy existing Dockerfile and insert --platform=${BUILDPLATFORM} into Dockerfile.cross, and preserve the original Dockerfile
	sed -e '1 s/\(^FROM\)/FROM --platform=\$$\{BUILDPLATFORM\}/; t' -e ' 1,// s//FROM --platform=\$$\{BUILDPLATFORM\}/' Dockerfile > Dockerfile.cross
	$(CONTAINER_TOOL) buildx create --name project-v3-builder
	$(CONTAINER_TOOL) buildx use project-v3-builder
	$(CONTAINER_TOOL) buildx build --platform=$(PLATFORMS) --push -f Dockerfile.cross -t ${PROJECT}/browser_service -t ${PROJECT}/browser_service:${VERSION} .
	$(CONTAINER_TOOL) buildx rm project-v3-builder
	rm Dockerfile.cross

maybe_docker_push:
	@docker manifest inspect $(PROJECT)/browser_service:$(VERSION) >/dev/null && echo "Image exists" || $(MAKE) dockerx
