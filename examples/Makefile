.PHONY: chatbot, chatbot_push

PROJECT ?= docker.io/eidolonai
VERSION := $(shell grep -m 1 '^version = ' pyproject.toml | awk -F '"' '{print $$2}')
SDK_VERSION := $(shell grep -m 1 '^version = ' ../sdk/pyproject.toml | awk -F '"' '{print $$2}')

# Define the directories
EIDOLON_SDK_DIR := ../sdk/eidolon_ai_sdk

# The target depends on all files in the eidolon_ai_sdk and docs directories
chatbot:
	docker build --build-arg LOC=eidolon_examples/conversational_chatbot --build-arg EIDOLON_VERSION=${SDK_VERSION} -t ${PROJECT}/chatbot -t ${PROJECT}/chatbot:${VERSION} .

chatbot_push: chatbot
	docker push ${PROJECT}/chatbot
	docker push ${PROJECT}/chatbot:${VERSION}

chatbot_bash: chatbot
	docker run --rm -it --entrypoint bash eidolonai/chatbot:latest
