import importlib
from typing import Type


def for_name(implementation_fqn: str, sub_class: Type) -> Type:
    """
    Dynamically imports a class and validates that it is a subclass of a specified type.

    Given a fully qualified class name (FQN) and a subclass type, this function dynamically imports
    the class from the FQN and checks whether it is a subclass of the specified subclass type. If the
    class can be imported and is a verified subclass, the class itself is returned. Otherwise, an error
    is raised.

    Parameters:
    - implementation_fqn (str): The fully qualified name of the class to import, in the form 'module.ClassName'.
    - sub_class (Type): The class type to check against the dynamically imported class.

    Returns:
    - Type: The imported class type that is a subclass of the specified `sub_class`.

    Raises:
    - ValueError: If the `implementation_fqn` is not provided, the class cannot be imported, the class
                  does not exist, or the imported class is not a subclass of `sub_class`.

    Note:
    - The fully qualified name of the class is case-sensitive and must be correct.
    """

    if implementation_fqn:
        module_name, class_name = implementation_fqn.rsplit(".", 1)
        try:
            module = importlib.import_module(module_name)
            implementation_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            raise ValueError(f"Unable to import {implementation_fqn}")
        if implementation_class and issubclass(implementation_class, sub_class):
            return implementation_class
        else:
            print(implementation_class)
            print(sub_class)
            print(issubclass(implementation_class, sub_class))
            raise ValueError(
                f"Implementation class '{implementation_fqn}' not found or is not a subclass of '{sub_class}'.")
    raise ValueError("Implementation not provided.")


def fqn(clazz=Type):
    return clazz.__module__ + '.' + clazz.__name__
