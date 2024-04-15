from fastapi import UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel
from pydub import AudioSegment

from eidolon_ai_sdk.agent.agent import register_program, Agent, AgentState
from eidolon_ai_sdk.agent.generic_agent import GenericAgentSpec
from eidolon_ai_sdk.cpu.agent_cpu import APU
from eidolon_ai_sdk.cpu.agent_io import SystemAPUMessage, UserTextAPUMessage
from eidolon_ai_sdk.cpu.llm.open_ai_speech import OpenAiSpeech
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class AutonomousSpeechAgentSpec(GenericAgentSpec):
    speech_llm: AnnotatedReference[OpenAiSpeech]
    cpu: AnnotatedReference[APU]


class LlmResponse(BaseModel):
    response: str


class AutonomousSpeechAgent(Agent, Specable[AutonomousSpeechAgentSpec]):
    speech_llm: OpenAiSpeech

    def __init__(self, spec: AutonomousSpeechAgentSpec):
        super().__init__(spec=spec)
        self.speech_llm = self.spec.speech_llm.instantiate(processing_unit_locator=None)
        self.cpu = self.spec.cpu.instantiate()

    async def call_llm(self, process_id, text: str):
        schema = LlmResponse.model_json_schema()
        schema["type"] = "object"

        t = await self.cpu.main_thread(process_id)
        await t.set_boot_messages(SystemAPUMessage(prompt=self.spec.system_prompt))

        response = await t.run_request([UserTextAPUMessage(prompt=text)], output_format=schema)
        response = LlmResponse(**response)
        return AgentState(name="idle", data=response)

    @register_program()
    async def speech_question(self, process_id, file: UploadFile = File(...)) -> bytes:
        audio = AudioSegment.from_file(file.file.read())
        # Convert to mp3
        audio_mp3 = audio.export("audio.mp3", format="mp3")

        text = await self.speech_llm.speech_to_text(audio_mp3)
        result = await self.call_llm(process_id, text)
        text_result = result.data.response
        audio_result = await self.speech_llm.text_to_speech(text_result)
        return Response(content=audio_result, media_type=audio.content_type)
