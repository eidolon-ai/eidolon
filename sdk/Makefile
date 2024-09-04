.PHONY: docker push_image dockerx maybe_docker_push

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep -m 1 '^version = ' pyproject.toml | awk -F '"' '{print $$2}')

poetry.lock: pyproject.toml
	poetry lock --no-update

docker: poetry.lock
	docker build --target sdk_base -t ${PROJECT}/sdk_base -t ${PROJECT}/sdk_base:${VERSION} -f ../Dockerfile ..
	docker build -t ${PROJECT}/sdk -t ${PROJECT}/sdk:${VERSION} -f ../Dockerfile ..

PLATFORMS ?= linux/arm64,linux/amd64
CONTAINER_TOOL ?= docker

dockerx:
	# copy existing Dockerfile and insert --platform=${BUILDPLATFORM} into Dockerfile.cross, and preserve the original Dockerfile
	sed -e '1 s/\(^FROM\)/FROM --platform=\$$\{BUILDPLATFORM\}/; t' -e ' 1,// s//FROM --platform=\$$\{BUILDPLATFORM\}/' ../Dockerfile > ../Dockerfile.cross
	$(CONTAINER_TOOL) buildx create --name project-v3-builder
	$(CONTAINER_TOOL) buildx use project-v3-builder
	$(CONTAINER_TOOL) buildx build --platform=$(PLATFORMS) --push -f ../Dockerfile.cross --target sdk_base -t ${PROJECT}/sdk_base -t ${PROJECT}/sdk_base:${VERSION}  ..
	$(CONTAINER_TOOL) buildx build --platform=$(PLATFORMS) --push -f ../Dockerfile.cross -t ${PROJECT}/sdk -t ${PROJECT}/sdk:${VERSION} ..
	$(CONTAINER_TOOL) buildx rm project-v3-builder
	rm ../Dockerfile.cross

maybe_docker_push:
	@docker manifest inspect $(PROJECT)/sdk:$(VERSION) >/dev/null && echo "Image exists" || $(MAKE) dockerx
