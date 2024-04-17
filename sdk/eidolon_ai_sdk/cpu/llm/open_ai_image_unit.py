import base64
from io import BytesIO
from typing import List, Literal, Tuple, Optional

from PIL import Image
from openai.types.chat import ChatCompletion
from pydantic import Field

from eidolon_ai_client.events import FileHandle
from eidolon_ai_client.util.logger import logger as eidolon_logger
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.image_unit import ImageUnitSpec, ImageUnit, ImageCreationCapabilities
from eidolon_ai_sdk.cpu.llm.open_ai_connection_handler import OpenAIConnectionHandler
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Specable
from eidolon_ai_sdk.util.image_utils import scale_image

logger = eidolon_logger.getChild("llm_unit")


class OpenAIImageUnitSpec(ImageUnitSpec):
    connection_handler: AnnotatedReference[OpenAIConnectionHandler]
    image_to_text_model: str = Field(default="gpt-4-vision-preview", description="The model to use for the vision LLM.")
    text_to_image_model: str = Field(default="dall-e-3", description="The model to use for the vision LLM.")
    temperature: float = 0.3
    image_to_text_system_prompt: str = Field(
        "You are an expert at answering questions about images. "
        "You are presented with an image and a question and must answer the question based on the information in the image.",
        description="The system prompt to use for text to image.",
    )


class OpenAIImageUnit(ImageUnit, Specable[OpenAIImageUnitSpec]):
    connection_handler: OpenAIConnectionHandler

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.connection_handler = self.spec.connection_handler.instantiate()

    def get_capabilities(self) -> ImageCreationCapabilities:
        return ImageCreationCapabilities(
            qualities=["standard", "hd"],
            sizes=[(1024, 1024), (1792, 1024), (1024, 1792)],
            styles=[
                "vivid",
                "natural",
            ],
            max_prompt_size=4000,
        )

    async def _image_to_text(self, prompt: str, image: bytes) -> str:
        """
        Converts an image to text.

        Args:
            image (bytes): The image data.

        Returns:
            str: The text.
            :param image:
            :param prompt:
        """
        # scale the image such that the max size of the shortest size is at most 768px
        data = scale_image(image)
        # base64 encode the data
        base64_image = base64.b64encode(data).decode("utf-8")
        messages = [
            {"role": "system", "content": self.spec.image_to_text_system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ]
        request = {
            "messages": messages,
            "model": self.spec.image_to_text_model,
            "temperature": self.spec.temperature,
        }

        result: ChatCompletion = await self.connection_handler.completion(**request)
        print(result)
        return result.choices[0].message.content

    async def _text_to_image(
        self,
        call_context: CallContext,
        text: str,
        quality: Optional[str] = None,
        size: Tuple[int, int] = (1024, 1024),
        style: Optional[str] = None,
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
        if quality is None:
            quality = "standard"
        if style is None:
            style = "natural"

        size_to_request = self._choose_optimal_size(size, self.get_capabilities().sizes)
        request = {
            "prompt": text,
            "model": self.spec.text_to_image_model,
            "response_format": "b64_json",
            "quality": quality,
            "size": f"{size_to_request[0]}x{size_to_request[1]}",
            "style": style,
        }
        result = await self.connection_handler.generate_image(**request)
        file_handles = []
        for i in result.data:
            image_data = base64.b64decode(i.b64_json)
            image = Image.open(BytesIO(image_data))
            image_fp = BytesIO()
            image.resize(size)
            image.save(image_fp, format=image_format)
            file_handles.append(
                await AgentOS.process_file_system.write_file(
                    call_context.process_id,
                    image_fp.getvalue(),
                    file_md={"prompt_rewrite": i.revised_prompt, "mimetype": f"image/{image_format}"},
                )
            )

        return file_handles

    def _choose_optimal_size(self, size: Tuple[int, int], sizes: List[Tuple[int, int]]) -> Tuple[int, int]:
        desired_width, desired_height = size
        aspect_ratio = desired_width / desired_height

        min_diff = float("inf")
        optimal_size = None

        for width, height in sizes:
            current_aspect_ratio = width / height
            diff = abs(aspect_ratio - current_aspect_ratio)

            if diff < min_diff:
                min_diff = diff
                optimal_size = (width, height)

        return optimal_size
