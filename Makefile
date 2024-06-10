.PHONY: force lock version publish

ALL_POETRY_PROJECTS := $(dir $(shell find . -name 'pyproject.toml'))
UNVERSIONED_PROJECTS := %scripts/ %usage-server/
UPUBLISHED_PROJECTS := $(UNVERSIONED_PROJECTS) %examples/

lock: $(addsuffix .lock, $(ALL_POETRY_PROJECTS))
	@echo "Done!"

version: $(addsuffix .version, $(filter-out $(UNVERSIONED_PROJECTS),$(ALL_POETRY_PROJECTS))) webui/.version
	@echo "Done!"

publish: $(addsuffix .publish, $(filter-out $(UPUBLISHED_PROJECTS),$(ALL_POETRY_PROJECTS)))
	@echo "Done!"

webui/.version: force
	@make -s -C scripts run "update_next webui";

# targets need to be defined as part of first expansion so we can grab dependencies from second expansion
.SECONDEXPANSION:

$(addsuffix .lock, $(ALL_POETRY_PROJECTS)): %.lock: force
	cd $*; poetry lock --no-update;

$(addsuffix .version, $(ALL_POETRY_PROJECTS)): %.version: force $$(shell make -C scripts -s run "get_deps $$* --suffix .version")
	@make -s -C scripts run "update_poetry ${*}";
	@cd $*; poetry lock --no-update;

$(addsuffix .publish, $(ALL_POETRY_PROJECTS)): %.publish: force $$(shell make -C scripts -s run "get_deps $$* --suffix .publish");
	@PACKAGE_NAME=$(shell grep -m 1 '^name = ' $*/pyproject.toml | awk -F '"' '{print $$2}'); \
	CURRENT_VERSION=$(shell grep -m 1 '^version = ' $*/pyproject.toml | awk -F '"' '{print $$2}'); \
	if ! pip index versions $$PACKAGE_NAME 2>/dev/null | grep -q $$CURRENT_VERSION; then \
		echo "Version $$CURRENT_VERSION of $$PACKAGE_NAME is not published on PyPI. Publishing now..."; \
		cd $*; poetry install; poetry publish --build; \
	else \
		echo "Version $$CURRENT_VERSION of $$PACKAGE_NAME is already published on PyPI."; \
	fi;