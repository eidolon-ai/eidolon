from typing import Optional, Literal

from eidolon_ai_client.events import FileHandle
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function


class AudioUnit(LogicUnit):
    @llm_function()
    async def text_to_speech(self, text: str, response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3") -> str:
        """
        Converts text to speech. The result of the call is a file handle that should be returned to the user unchanged.

        Args:
            text (str): The text to convert to speech.

        Returns:
            FileHandle: A file handle that contains the audio data.
            :param text:
            :param response_format: Response audio format. Legal values are ["mp3", "opus", "aac", "flac", "wav", "pcm"].  Defaults to "mp3".
        """
        audio = await self._text_to_speech(text, response_format)
        handle = await AgentOS.process_file_system.write_file(RequestContext.get("process_id"), audio, {"mimetype": f"audio/{response_format}"})
        return handle.get_url()

    async def _text_to_speech(self, text: str, response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3") -> bytes:
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

    @llm_function()
    async def speech_to_text(
        self, audio: FileHandle, prompt: Optional[str] = None, language: Optional[str] = None
    ) -> str:
        """
        Converts speech to text.

        Args:
            audio (FileHandle): A file handle to the audio data.
            prompt (Optional[str], optional): An optional text to guide the model's style or continue a previous audio segment. Defaults to None.
            language (Optional[str], optional): The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency.
        Returns:
            str: The result of the conversion
            :param audio: A file handle to the audio data.
            :param prompt: An optional text to guide the model's style or continue a previous audio segment. Defaults to the built-in prompt.
            :param language: The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency. This parameter is optional.
        """
        audio_data, metadata = await AgentOS.process_file_system.read_file(RequestContext.get("process_id"), audio.file_id)
        return await self._speech_to_text(audio_data, metadata.get("mimetype", "audio/wav"), prompt, language)

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
            :param prompt:
            :param language:
            :param mime_type:
        """
