import os


def replace_env_var_in_string(s, **defaults):
    """
    Replace all occurrences of '${VAR}' with the value of the VAR environment variable.
    """
    for key in os.environ:
        replacement = os.environ.get(key, defaults[key]) if key in defaults else os.environ[key]
        s = s.replace(f"${{{key}}}", replacement)
    return s
