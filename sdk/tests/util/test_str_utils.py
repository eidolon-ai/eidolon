import os

import pytest

from eidos_sdk.util.str_utils import replace_env_var_in_string


class TestStrUtils:
    # Test fixture to set environment variables
    @pytest.fixture(autouse=True)
    def set_env_vars(self):
        os.environ["FOO"] = "/somepath"
        os.environ["BAR"] = "/anotherpath"
        yield  # this line is where the testing happens
        # Teardown (if necessary)
        del os.environ["FOO"]
        del os.environ["BAR"]

    def test_single_replacement(self):
        assert replace_env_var_in_string("Path: ${FOO}/app") == "Path: /somepath/app"

    def test_no_replacement(self):
        assert replace_env_var_in_string("Path: /not_an_env_var/app") == "Path: /not_an_env_var/app"

    def test_multiple_replacements_same_var(self):
        assert replace_env_var_in_string("${FOO}/app and ${FOO}/bin") == "/somepath/app and /somepath/bin"

    def test_multiple_replacements_different_vars(self):
        assert replace_env_var_in_string("${FOO}/app and ${BAR}/bin") == "/somepath/app and /anotherpath/bin"

    def test_no_variables(self):
        assert replace_env_var_in_string("Just a normal string.") == "Just a normal string."

    def test_empty_string(self):
        assert replace_env_var_in_string("") == ""

    def test_only_variable(self):
        assert replace_env_var_in_string("${FOO}") == "/somepath"

    def test_nonexistent_variable(self):
        assert replace_env_var_in_string("Path: ${NONEXISTENT}/app") == "Path: ${NONEXISTENT}/app"

    def test_variable_surrounded_by_text(self):
        assert replace_env_var_in_string("Path: pre_${FOO}_post/app") == "Path: pre_/somepath_post/app"
