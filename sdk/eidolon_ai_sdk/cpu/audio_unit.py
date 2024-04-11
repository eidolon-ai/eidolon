from typing import Optional

from pydantic import BaseModel

from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Specable


class AudioUnitSpec(BaseModel):
    pass


class AudioUnit(ProcessingUnit, Specable[AudioUnitSpec]):
    def __init__(self, spec: AudioUnitSpec = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    async def text_to_speech(self, text: str, response_format: str = "mp3") -> bytes:
        """
        Converts text to speech.

        Args:
            text (str): The text to convert to speech.

        Returns:
            bytes: The audio data.
            :param text:
            :param response_format: Response audio format. Legal values are ["mp3", "opus", "aac", "flac", "wav", "pcm"].  Defaults to "mp3".
        """
        raise NotImplementedError("generate_audio not implemented")

    async def speech_to_text(
        self, audio: bytes, mime_type: str, prompt: Optional[str] = None, language: Optional[str] = None
    ) -> str:
        """
        Converts speech to text.

        Args:
            audio (bytes): The audio data.
            prompt (Optional[str], optional): An optional text to guide the model's style or continue a previous audio segment. Defaults to None.
            language (Optional[str], optional): The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency.
        Returns:
            str: The text.
            :param audio:
            :param prompt:
            :param language:
            :param mime_type:
        """
