import importlib
from typing import Type


def for_name(implementation_fqn: str, sub_class: Type = object) -> Type:
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
        try:
            module_name, class_name = implementation_fqn.rsplit(".", 1)
        except ValueError:
            raise ValueError(f"'{implementation_fqn}' is not a valid fully qualified class name.")
        try:
            module = importlib.import_module(module_name)
            implementation_class = getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            print(e)
            raise ValueError(f"Unable to import {implementation_fqn}")
        if implementation_class and issubclass(implementation_class, sub_class):
            return implementation_class
        else:
            print(implementation_class)
            print(sub_class)
            print(issubclass(implementation_class, sub_class))
            raise ValueError(
                f"Implementation class '{implementation_fqn}' not found or is not a subclass of '{sub_class}'."
            )
    raise ValueError("Implementation not provided.")


def fqn(clazz=Type) -> str:
    return clazz.__module__ + "." + clazz.__name__


def get_function_details(func):
    function_name = func.__name__
    owning_class = None

    if hasattr(func, "__self__"):
        # This is a bound method; it will have a '__self__' attribute.
        owning_class = func.__self__.__class__.__name__
    elif hasattr(func, "__qualname__"):
        # This is an unbound method or a function; try to parse the class name out of the __qualname__
        qualname_parts = func.__qualname__.split(".")
        if len(qualname_parts) > 1:
            owning_class = qualname_parts[-2]

    return function_name, owning_class
