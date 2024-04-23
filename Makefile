.SECONDEXPANSION:
$(wildcard **/pyproject.toml): %/pyproject.toml : $$(filter-out $$@, $$(wildcard %/*)) $$(wildcard %/**/*) $$(shell cd scripts && poetry run get_deps --loc % --workdir .. --suffix pyproject.toml)
	@#echo "Dependencies: $^"
	cd $*; poetry version patch;
