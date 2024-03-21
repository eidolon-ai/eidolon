from typing import Annotated

from fastapi import UploadFile, File, Body
from pydub import AudioSegment
from starlette.responses import Response

from eidolon_ai_sdk.agent.agent import AgentSpec, Agent, register_program
from eidolon_ai_sdk.cpu.llm.open_ai_speech import OpenAiSpeech
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Specable


class AutonomousSpeechAgentSpec(AgentSpec):
    speech_llm: AnnotatedReference[OpenAiSpeech]


class AutonomousSpeechAgent(Agent, Specable[AutonomousSpeechAgentSpec]):
    speech_llm: OpenAiSpeech

    def __init__(self, spec: AutonomousSpeechAgentSpec):
        super().__init__(spec=spec)
        self.speech_llm = self.spec.speech_llm.instantiate()
        self.cpu = self.spec.cpu.instantiate()

    @register_program()
    async def speech_to_text(self, process_id, file: UploadFile = File(...)) -> str:
        audio = AudioSegment.from_file(file.file.read())
        # Convert to mp3
        audio_mp3 = audio.export("audio.mp3", format="mp3")

        text = await self.speech_llm.speech_to_text(audio_mp3)
        return text

    @register_program()
    async def speech_to_text(self, text: Annotated[str, Body(description="The text to speak", embed=True)]):
        audio_result = await self.speech_llm.text_to_speech(text)
        return Response(audio_result, 200, media_type="audio/mpeg")
