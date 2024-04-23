VERSIONED_POETRY_PROJECTS := $(filter-out scripts,$(dir $(shell find . -name 'pyproject.toml')))
VERSIONED_TOML_FILES := $(addsuffix pyproject.toml, $(VERSIONED_POETRY_PROJECTS))
PYPI_PUBLISH_TARGETS := $(addsuffix .pypi_published, $(filter-out examples,$(VERSIONED_POETRY_PROJECTS)))
.PHONY: update_deps publish_pypi

update_deps: $(VERSIONED_TOML_FILES)
	@echo "Done!"

publish_pypi: $(PYPI_PUBLISH_TARGETS) update_deps
	@echo "Done!"

.SECONDEXPANSION:
$(VERSIONED_TOML_FILES): %/pyproject.toml: \
$$(filter-out %/pyproject.toml %/poetry.lock %/pypi_publish_version, $$(shell find % -type f -not -path "*/tests/*" -not -path "*/dist/*" | sed 's/ /\\ /g')) \
$$(shell cd scripts && poetry run get_deps --loc % --workdir .. --suffix pyproject.toml)
	@echo "Updating $*";
	@cd scripts; poetry run update_deps ../$*;
	@cd $*; poetry version patch;
	@cd $*; poetry lock --no-update;

$(PYPI_PUBLISH_TARGETS): %/.pypi_published: %/pyproject.toml
	@#cd $*; poetry publish --build;
	@echo $(shell grep -m 1 '^version = ' $*/pyproject.toml | awk -F '"' '{print $$2}') > $*/pypi_publish_version
