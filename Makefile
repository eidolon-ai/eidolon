PYPROJECT_FILES := $(shell find . -name 'pyproject.toml')

.SECONDEXPANSION:
$(PYPROJECT_FILES): %/pyproject.toml: \
$$(filter-out %/pyproject.toml %/poetry.lock %/pypi_publish.json, $$(shell find % -type f -not -path "*/tests/*" -not -path "*/dist/*" | sed 's/ /\\ /g')) \
$$(shell cd scripts && poetry run get_deps --loc % --workdir .. --suffix pyproject.toml)
	@echo "Updating $*";
	@cd scripts; poetry run update_deps ../$*;
	@cd $*; poetry version patch;
	@cd $*; poetry lock --no-update;


.PHONY: update_deps
update_deps: $(PYPROJECT_FILES)
	@echo "Done!"


PYPI_FILES := $(shell find . -name 'pypi_publish.json')
$(PYPI_FILES): %/pypi_publish.json: %/pyproject.toml
	@cd $*; poetry build;  # todo, publish later
	@echo $(shell grep -m 1 '^version = ' $*/pyproject.toml | awk -F '"' '{print $$2}') > $*/pypi_publish.json
