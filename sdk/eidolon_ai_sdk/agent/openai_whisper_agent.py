from typing import Annotated

from fastapi import Body

from eidolon_ai_sdk.agent.agent import AgentSpec, Agent, register_program
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.llm.open_ai_speech import OpenAiSpeech
from eidolon_ai_sdk.system.process_file_system import FileHandle
from eidolon_ai_sdk.system.processes import ProcessDoc
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
    async def speech_to_text(
        self, process_id, audio: Annotated[FileHandle, Body(description="The audio file", embed=True)]
    ):
        await ProcessDoc.set_delete_on_terminate(process_id, True)
        file, metadata = await AgentOS.process_file_system.read_file(process_id, audio.file_id)
        mimetype = "audio/wav"
        if metadata and "mimetype" in metadata:
            mimetype = metadata["mimetype"]
        # audio = AudioSegment.from_file(file)
        # # Convert to mp3
        # audio_mp3 = audio.export("audio.mp3", format="mp3")

        text = await self.speech_llm.speech_to_text(file, mimetype)
        return {"response": text}

    @register_program()
    async def text_to_speech(
        self, process_id: str, text: Annotated[str, Body(description="The text to speak", embed=True)]
    ) -> FileHandle:
        audio_result = await self.speech_llm.text_to_speech(text)
        file_id = await AgentOS.process_file_system.write_file(process_id, audio_result, {"mimetype": "audio/mpeg"})

        return FileHandle(machineURL=AgentOS.current_machine_url(), process_id=process_id, file_id=file_id)
