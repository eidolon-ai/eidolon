VERSIONED_POETRY_PROJECTS := $(filter-out ./scripts/,$(dir $(shell find . -name 'pyproject.toml')))
VERSIONED_TOML_FILES := $(addsuffix pyproject.toml, $(VERSIONED_POETRY_PROJECTS))
PYPI_PUBLISH_TARGETS := $(addsuffix .pypi_published, $(filter-out ./examples/,$(VERSIONED_POETRY_PROJECTS)))
.PHONY: update_deps publish_pypi

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

# Our publish targets (.pypi_published) depend on their the pyproject.toml file and upstream publish targets
# These files represent the last version of the package published to PyPI
$(PYPI_PUBLISH_TARGETS): %/.pypi_published: %/pyproject.toml \
$$(shell make -C scripts run "get_deps --loc $$* --workdir .. --suffix p.pypi_published")
	@#cd $*; poetry publish --build;
	@echo $(shell grep -m 1 '^version = ' $*/pyproject.toml | awk -F '"' '{print $$2}') > $*/pypi_publish_version
