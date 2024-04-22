.SECONDEXPANSION:
$(wildcard **/pyproject.toml): %/pyproject.toml : $$(filter-out $$@, $$(wildcard %/*))
	cd $*; poetry version patch;
