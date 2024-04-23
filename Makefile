ALL_POETRY_PROJECTS := $(dir $(shell find . -name 'pyproject.toml'))
UNVERSIONED_PROJECTS := ./scripts/ ./usage-service/usage-server/

VERSIONED_POETRY_PROJECTS := $(filter-out $(UNVERSIONED_PROJECTS),$(ALL_POETRY_PROJECTS))
VERSIONED_TOML_FILES := $(addsuffix pyproject.toml, $(VERSIONED_POETRY_PROJECTS))

UPUBLISHED_PROJECTS := $(UNVERSIONED_PROJECTS) ./examples/
PUBLISHED_POETRY_PROJECTS := $(filter-out $(UPUBLISHED_PROJECTS),$(ALL_POETRY_PROJECTS))
PYPI_PUBLISH_TARGETS := $(addsuffix .pypi_phony, $(PUBLISHED_POETRY_PROJECTS))

.PHONY: update_deps publish_pypi $(PYPI_PUBLISH_TARGETS)

update_deps: $(VERSIONED_TOML_FILES)
	@echo "Done!"

publish_pypi: $(PYPI_PUBLISH_TARGETS)
	@echo "Done!"

.SECONDEXPANSION:

# Our pyproject.toml files depend on everything in the project directory except and upstream pyproject.toml files
$(VERSIONED_TOML_FILES): %/pyproject.toml: \
$$(filter-out %/pyproject.toml %/poetry.lock %/pypi_publish_version, $$(shell find % -type f -not -path "*/tests/*" -not -path "*/dist/*" | sed 's/ /\\ /g')) \
$$(shell make -C scripts run "get_deps --loc $$* --workdir .. --suffix pyproject.toml")
	@echo "Updating $*";
	@make -C scripts run "update_deps ../${*}";
	@cd $*; poetry version patch;
	@cd $*; poetry lock --no-update;


# Our publish targets (.pypi_published) depend on their the pyproject.toml file and upstream publish targets (to make sure we publish in proper order)
$(PYPI_PUBLISH_TARGETS): %/.pypi_phony: %/pyproject.toml \
$$(shell make -C scripts run "get_deps --loc $$* --workdir .. --suffix .pypi_phony");
	@PACKAGE_NAME=$(shell grep -m 1 '^name = ' $*/pyproject.toml | awk -F '"' '{print $$2}'); \
	CURRENT_VERSION=$(shell grep -m 1 '^version = ' $*/pyproject.toml | awk -F '"' '{print $$2}'); \
	if ! pip index versions $$PACKAGE_NAME 2>/dev/null | grep -q $$CURRENT_VERSION; then \
		echo "Version $$CURRENT_VERSION of $$PACKAGE_NAME is not published on PyPI. Publishing now..."; \
		cd $*; poetry publish --build; \
	else \
		echo "Version $$CURRENT_VERSION of $$PACKAGE_NAME is already published on PyPI."; \
	fi;
