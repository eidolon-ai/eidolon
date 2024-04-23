VERSION ?= prepatch
PYPROJECT_FILES := $(shell find . -name 'pyproject.toml')

.SECONDEXPANSION:
$(PYPROJECT_FILES): %/pyproject.toml: \
$$(filter-out %/pyproject.toml %/poetry.lock, $$(shell find % -type f | sed 's/ /\\ /g')) \
$$(shell cd scripts && poetry run get_deps --loc % --workdir .. --suffix pyproject.toml)
	@echo "Updating $*";
	@cd $*; poetry version $(VERSION);


.PHONY: update_deps
update_deps: $(PYPROJECT_FILES)
	@echo "Updated dependencies"