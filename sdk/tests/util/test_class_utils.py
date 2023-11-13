import importlib
import sys
from importlib.util import module_from_spec

import pytest

from eidolon_sdk.util.class_utils import for_name


# Test class for grouping the tests
class TestForName:

    # Setup method to create a sample module with classes for testing
    @classmethod
    def setup_class(cls):
        # Create a temporary module with classes for testing
        cls.temp_module_name = 'temp_test_module'
        cls.temp_module = module_from_spec(
            importlib.util.spec_from_loader(cls.temp_module_name, loader=None)
        )
        cls.base_class = type('BaseClass', (object,), {})
        cls.sub_class = type('SubClass', (cls.base_class,), {})
        cls.non_sub_class = type('NonSubClass', (object,), {})
        setattr(cls.temp_module, 'BaseClass', cls.base_class)
        setattr(cls.temp_module, 'SubClass', cls.sub_class)
        setattr(cls.temp_module, 'NonSubClass', cls.non_sub_class)
        sys.modules[cls.temp_module_name] = cls.temp_module

    # Teardown method to clean up the temporary module
    @classmethod
    def teardown_class(cls):
        del sys.modules[cls.temp_module_name]

    def test_successful_import_and_subclass_check(self):
        """Test successful dynamic import and subclass check."""
        result = for_name(f'{self.temp_module_name}.SubClass', self.base_class)
        assert result is self.sub_class

    def test_implementation_fqn_not_provided(self):
        """Test error when the fully qualified name is not provided."""
        with pytest.raises(ValueError) as exc_info:
            for_name('', self.base_class)
        assert "Implementation not provided" in str(exc_info.value)

    def test_implementation_fqn_incorrect(self):
        """Test error when the fully qualified name is incorrect."""
        with pytest.raises(ValueError) as exc_info:
            for_name(f'{self.temp_module_name}.NonExistentClass', self.base_class)
        assert "Unable to import" in str(exc_info.value)

    def test_implementation_class_not_subclass(self):
        """Test error when the class is not a subclass of the specified type."""
        with pytest.raises(ValueError) as exc_info:
            for_name(f'{self.temp_module_name}.NonSubClass', self.sub_class)
        assert "not found or is not a subclass" in str(exc_info.value)

# You can run these tests by executing the command `pytest test_dynamic_importer.py`
# in your terminal, assuming `test_dynamic_importer.py` is the name of the file containing these tests.
