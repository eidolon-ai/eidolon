.PHONY: run

.make_poetry_install: poetry.lock
	poetry install
	touch .make_poetry_install

pyproject.toml:

poetry.lock: pyproject.toml
	poetry lock --no-update

run: .make_poetry_install
	@poetry run $(filter-out $@,$(MAKECMDGOALS))

%:
	@:
