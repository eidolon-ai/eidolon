import os


def replace_env_var_in_string(s, **defaults):
    """
    Replace all occurrences of '${VAR}' with the value of the VAR environment variable.
    """
    for key in {*os.environ, *defaults.keys()}:
        replacement = os.environ.get(key, defaults[key]) if key in defaults else os.environ[key]
        s = s.replace(f"${{{key}}}", replacement)
    return s


def format_frame_info(frame_info):
    return f'File "{frame_info.filename}", line {frame_info.lineno}, in {frame_info.function}\n    {frame_info.code_context[0].strip()}'
