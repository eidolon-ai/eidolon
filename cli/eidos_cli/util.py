from rich.text import Text


def rt(text: str, style: str = ""):
    """Render text with style."""
    return Text(text, style=style, end="")
