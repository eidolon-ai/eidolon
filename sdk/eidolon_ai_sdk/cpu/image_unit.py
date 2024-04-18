from typing import List, Tuple, Literal, Optional

from pydantic import BaseModel, Field

from eidolon_ai_client.events import FileHandle
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.logic_unit import llm_function, LogicUnit
from eidolon_ai_sdk.system.reference_model import Specable


class ImageCreationCapabilities(BaseModel):
    qualities: List[str]
    sizes: List[Tuple[int, int]]
    styles: List[str]
    max_prompt_size: int


class ImageUnitSpec(BaseModel):
    image_to_text_prompt: str = Field(default="Use the following prompt to describe the image:", description="The prompt to use for the conversion. The text should be very verbose and detailed.")
    text_to_image_prompt: str = Field(default="Use the provided text to create an image:", description="The prompt to use for the conversion. The text should be very verbose and detailed.")


class ImageUnit(LogicUnit, Specable[ImageUnitSpec]):
    def __init__(self, spec: ImageUnitSpec = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    def get_capabilities(self) -> ImageCreationCapabilities:
        raise NotImplementedError("get_capabilities not implemented")

    @llm_function()
    async def image_to_text(self, prompt: str, image: FileHandle) -> str:
        """
        Converts an image to text. The result of the call is the text that describes the image.
        :param image: A file handle to the image data.
        :param prompt: The prompt to use for the conversion. The text should be very verbose and detailed.
        :return:
        """
        message = self.spec.image_to_text_prompt
        if prompt:
            message += "\n" + prompt
        data, metadata = await AgentOS.process_file_system.read_file(RequestContext.get("process_id"), image.file_id)
        return await self._image_to_text(message, data)

    async def _image_to_text(self, prompt: str, image: bytes) -> str:
        """
        Converts an image to text.

        Args:
            image (bytes): The image data.

        Returns:
            str: The text.
            :param image: A file handle to the image data.
            :param prompt: The prompt to use for the conversion. The text should be very verbose and detailed.
        """
        raise NotImplementedError("image_to_text not implemented")

    @llm_function()
    async def text_to_image(self, text: str, quality: Optional[str] = None, width: int = 1024, height: int = 1024, style: Optional[str] = None,
                            image_format: Literal["jpeg", "png", "tiff", "bmp", "webp"] = "webp") -> List[str]:
        """
        Converts text to one or more images. The result of the call is a list of file handles that should be returned to the user unchanged.
        :param width: The width of the image. Defaults to 1024.
        :param height: The height of the image. Defaults to 1024.
        :param text: The text to convert to an image. The text should be very verbose and detailed. The text CANNOT exceed 4000 characters
        :param quality: An optional quality level for the image. Legal values are ["standard", "hd"]. Defaults to "standard".
        :param style: An optional style for the image. Legal values are ["vivid", "natural"]. Defaults to None.
        :param image_format: The image format. Legal values are ["jpeg", "png", "tiff", "bmp", "webp"]. Defaults to "webp".
        :return:
        """
        message = self.spec.text_to_image_prompt + "\n" + text
        call_context = CallContext(process_id=RequestContext.get("process_id"))
        image_links = []
        for file_handle in await self._text_to_image(call_context, message, quality, (width, height), style, image_format):
            image_links.append(f"{file_handle.machineURL}/processes/{file_handle.process_id}/files/{file_handle.file_id}")
        return image_links

    async def _text_to_image(self, call_context: CallContext, text: str, quality: Optional[str] = None, size: Tuple[int, int] = (1024, 1024), style: Optional[str] = None,
                             image_format: Literal["jpeg", "png", "tiff", "bmp", "webp"] = "webp",
    ) -> List[FileHandle]:
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
