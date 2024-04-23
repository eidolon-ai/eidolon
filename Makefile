VERSION ?= patch
PYPROJECT_FILES := $(shell find . -name 'pyproject.toml')

.SECONDEXPANSION:
$(PYPROJECT_FILES): %/pyproject.toml: \
$$(filter-out %/pyproject.toml %/poetry.lock, $$(shell find % -type f -not -path "*/tests/*" | sed 's/ /\\ /g')) \
$$(shell cd scripts && poetry run get_deps --loc % --workdir .. --suffix pyproject.toml)
	@echo "Updating $*";
	@cd scripts; poetry run update_deps ../$*;
	@cd $*; poetry version $(VERSION);
	@cd $*; poetry lock --no-update;


.PHONY: update_deps
update_deps: $(PYPROJECT_FILES)
	@echo "Done!"