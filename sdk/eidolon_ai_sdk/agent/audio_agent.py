from typing import Annotated

from fastapi import Body
from pydantic import BaseModel

from eidolon_ai_client.events import FileHandle
from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.apu.audio_unit import AudioUnit
from eidolon_ai_sdk.system.processes import ProcessDoc
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from eidolon_ai_sdk.system.specable import Specable


class AutonomousSpeechAgentSpec(BaseModel):
    speech_llm: AnnotatedReference[AudioUnit]


class AutonomousSpeechAgent(Specable[AutonomousSpeechAgentSpec]):
    speech_llm: AudioUnit

    @register_program()
    async def speech_to_text(
        self, process_id, audio: Annotated[FileHandle, Body(description="The audio file", embed=True)]
    ):
        await ProcessDoc.set_delete_on_terminate(process_id, True)
        text = await self.speech_llm.speech_to_text(audio)
        return {"response": text}

    @register_program()
    async def text_to_speech(self, text: Annotated[str, Body(description="The text to speak", embed=True)]) -> str:
        return await self.speech_llm.text_to_speech(text)
