import os

from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory
from prompt_toolkit.validation import ValidationError, Validator
from rich.text import Text


def rt(text: str, style: str = ""):
    """Render text with style."""
    return Text(text, style=style, end="")


class NumberValidator(Validator):
    def __init__(self, allow_float: bool = False, allow_negative: bool = False):
        self.allow_float = allow_float
        self.allow_negative = allow_negative

    def validate(self, document: Document) -> None:
        text = document.text.strip()
        if self.allow_float:
            try:
                number = float(text)
            except ValueError:
                raise ValidationError(message="The input is not a valid float", cursor_position=len(text))
        else:
            try:
                number = int(text)
            except ValueError:
                raise ValidationError(message="The input is not a valid integer", cursor_position=len(text))
        if not self.allow_negative:
            if number < 0:
                raise ValidationError(message="This input cannot be negative", cursor_position=len(text))


class BooleanValidator(Validator):
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        legal_values = ["y", "yes", "n", "no", "0", "1", "", "true", "false"]
        if text.lower() not in legal_values:
            raise ValidationError(message=f"This input must be ont of {legal_values}", cursor_position=len(text))


class VarExpandingFileHistory(FileHistory):
    def __init__(self, filename: str):
        filename = os.path.expandvars(filename)
        filename = os.path.expanduser(filename)
        super().__init__(filename)


class RequiredValidator(Validator):
    def __init__(self, required: bool, nested_validator: Validator = None):
        super().__init__()
        self.required = required
        self.nested_validator = nested_validator

    def validate(self, document: Document) -> None:
        text = document.text.strip()
        if not text:
            if self.required:
                raise ValidationError(message="This input is required", cursor_position=len(text))
        elif self.nested_validator:
            self.nested_validator.validate(document)


class FilePathValidator(Validator):
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        text = os.path.expandvars(text)
        text = os.path.expanduser(text)
        if not os.path.isfile(text):
            raise ValidationError(message="This input is not a file", cursor_position=len(text))
