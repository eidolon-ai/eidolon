from pydantic import BaseModel

from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Specable


class ImageUnitSpec(BaseModel):
    pass


class ImageUnit(ProcessingUnit, Specable[ImageUnitSpec]):
    def __init__(self, spec: ImageUnitSpec = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    async def image_to_text(self, prompt: str, image: bytes) -> str:
        """
        Converts an image to text.

        Args:
            image (bytes): The image data.

        Returns:
            str: The text.
        """
        raise NotImplementedError("image_to_text not implemented")

    async def text_to_image(self, text: str) -> bytes:
        """
        Converts text to an image.

        Args:
            text (str): The text.

        Returns:
            bytes: The image data.
        """
        raise NotImplementedError("text_to_image not implemented")
