.PHONY: run

run: .make_poetry_install
	@poetry run $(filter-out $@,$(MAKECMDGOALS))

.make_poetry_install: poetry.lock
	@poetry install > /dev/null
	@touch .make_poetry_install

poetry.lock: pyproject.toml
	@poetry lock --no-update > /dev/null
	@touch poetry.lock

%:
	@:
