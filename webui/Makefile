.PHONY: docker push_image dockerx maybe_docker_push

PROJECT ?= docker.io/eidolonai
VERSION :=  $$(node -p "require('./package.json').version")

version:
	@echo $(VERSION)

docker:
	docker build -t ${PROJECT}/webui -t ${PROJECT}/webui:${VERSION} .

PLATFORMS ?= linux/arm64,linux/amd64
CONTAINER_TOOL ?= docker

dockerx:
	# copy existing Dockerfile and insert --platform=${BUILDPLATFORM} into Dockerfile.cross, and preserve the original Dockerfile
	sed -e '1 s/\(^FROM\)/FROM --platform=\$$\{BUILDPLATFORM\}/; t' -e ' 1,// s//FROM --platform=\$$\{BUILDPLATFORM\}/' Dockerfile > Dockerfile.cross
	$(CONTAINER_TOOL) buildx create --name project-v3-builder
	$(CONTAINER_TOOL) buildx use project-v3-builder
	$(CONTAINER_TOOL) buildx build --platform=$(PLATFORMS) --push -f Dockerfile.cross -t ${PROJECT}/webui -t ${PROJECT}/webui:${VERSION} .
	$(CONTAINER_TOOL) buildx rm project-v3-builder
	rm Dockerfile.cross

maybe_docker_push:
	@docker manifest inspect $(PROJECT)/webui:$(VERSION) >/dev/null && echo "Image exists" || { $(MAKE) dockerx; exit $$?; }
