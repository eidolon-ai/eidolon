from typing import List, Tuple, Literal, Optional

from pydantic import BaseModel

from eidolon_ai_client.events import FileHandle
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Specable


class ImageCreationCapabilities(BaseModel):
    qualities: List[str]
    sizes: List[Tuple[int, int]]
    styles: List[str]
    max_prompt_size: int


class ImageUnitSpec(BaseModel):
    pass


class ImageUnit(ProcessingUnit, Specable[ImageUnitSpec]):
    def __init__(self, spec: ImageUnitSpec = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    def get_capabilities(self) -> ImageCreationCapabilities:
        raise NotImplementedError("get_capabilities not implemented")

    async def image_to_text(self, prompt: str, image: bytes) -> str:
        """
        Converts an image to text.

        Args:
            image (bytes): The image data.

        Returns:
            str: The text.
            :param image:
            :param prompt:
        """
        raise NotImplementedError("image_to_text not implemented")

    async def text_to_image(self, call_context: CallContext, text: str, quality: Optional[str] = None, size: Tuple[int, int] = (1024, 1024), style: Optional[str] = None,
                            image_format: Literal["jpeg", "png", "tiff", "bmp", "webp"] = "webp") -> List[FileHandle]:
        """
        Converts text to an image.

        Args:
            text (str): The text.

        Returns:
            bytes: The image data.
            :param image_format:
            :param quality:
            :param size:
            :param style:
            :param text:
            :param call_context:
        """
        raise NotImplementedError("text_to_image not implemented")
