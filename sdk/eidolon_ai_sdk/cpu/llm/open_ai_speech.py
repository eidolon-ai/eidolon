from typing import Optional, Literal

from openai import AsyncOpenAI
from pydantic import Field, BaseModel

from eidolon_ai_sdk.cpu.audio_unit import AudioUnit
from eidolon_ai_sdk.system.reference_model import Specable


class OpenAiSpeechSpec(BaseModel):
    text_to_speech_model: Literal["tts-1", "tts-1-hd"] = Field(
        default="tts-1-hd", description="The model to use for text to speech."
    )
    text_to_speech_voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = Field(
        default="alloy", description="The voice to use for text to speech."
    )
    speech_to_text_model: Literal["whisper-1"] = Field(
        default="whisper-1", description="The model to use for speech to text."
    )
    speech_to_text_temperature: float = Field(
        default=0.3,
        description="The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.",
    )


class OpenAiSpeech(AudioUnit, Specable[OpenAiSpeechSpec]):
    model: str
    temperature: float
    llm: AsyncOpenAI = None

    def __init__(self, spec: OpenAiSpeechSpec, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, spec)

    async def _text_to_speech(self, text: str, response_format: str = "mp3") -> bytes:
        """
        Converts text to speech.

        Args:
            text (str): The text to convert to speech.

        Returns:
            bytes: The audio data.
            :param text:
            :param response_format: Response audio format. Legal values are ["mp3", "opus", "aac", "flac", "wav", "pcm"].  Defaults to "mp3".
        """
        if not self.llm:
            self.llm = AsyncOpenAI()

        response = await self.llm.audio.speech.create(
            model=self.spec.text_to_speech_model,
            voice=self.spec.text_to_speech_voice,
            response_format="mp3",
            input=text,
        )

        return response.content

    async def _speech_to_text(
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
            :param language:
            :param prompt:
            :param mime_type:
        """
        if not self.llm:
            self.llm = AsyncOpenAI()
        request = {
            "file": ("audio", audio, mime_type),
            "model": self.spec.speech_to_text_model,
            "temperature": self.spec.speech_to_text_temperature,
            "extra_headers": {"Content-Type": "multipart/form-data; boundary=eidolon-boundary"},  # WTF!!!! -- openai includes a rando boundary id. Bad for tests because it causes the cassettes uniqueness to fail.
        }

        if language:
            request["language"] = language

        if prompt:
            request["prompt"] = prompt

        response = await self.llm.audio.transcriptions.create(**request)

        return response.text
