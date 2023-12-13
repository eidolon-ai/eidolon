from fastapi import UploadFile, File
from fastapi.responses import Response
from pydub import AudioSegment

from eidos.agent.agent import register_program, Agent, AgentState
from eidos.agent.generic_agent import GenericAgentSpec, LlmResponse
from eidos.cpu.agent_cpu import AgentCPU
from eidos.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidos.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos.cpu.llm.open_ai_speech import OpenAiSpeech
from eidos.system.reference_model import Specable, AnnotatedReference


class AutonomousSpeechAgentSpec(GenericAgentSpec):
    speech_llm: AnnotatedReference[OpenAiSpeech, OpenAiSpeech]
    cpu: AnnotatedReference[AgentCPU, ConversationalAgentCPU]


class AutonomousSpeechAgent(Agent, Specable[AutonomousSpeechAgentSpec]):
    speech_llm: OpenAiSpeech

    def __init__(self, spec: AutonomousSpeechAgentSpec):
        super().__init__(spec=spec)
        self.speech_llm = self.spec.speech_llm.instantiate()
        self.cpu = self.spec.cpu.instantiate()

    async def call_llm(self, process_id, text: str):
        schema = LlmResponse.model_json_schema()
        schema["type"] = "object"

        t = await self.cpu.main_thread(process_id)
        await t.set_boot_messages(schema, SystemCPUMessage(prompt=self.spec.system_prompt))

        response = await t.schedule_request(prompts=[UserTextCPUMessage(prompt=text)], output_format=schema)
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
