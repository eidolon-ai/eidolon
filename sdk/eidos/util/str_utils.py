import os


def replace_env_var_in_string(s):
    """
    Replace all occurrences of '${VAR}' with the value of the VAR environment variable.
    """
    for key in os.environ:
        s = s.replace(f"${{{key}}}", os.environ[key])
    return s
