from fastapi import UploadFile, File
from fastapi.responses import Response
from pydub import AudioSegment

from eidos.agent.agent import register_program
from eidos.agent.generic_agent import GenericAgent, GenericAgentSpec
from eidos.cpu.llm.open_ai_speech import OpenAiSpeech
from eidos.system.reference_model import Reference, Specable


class AutonomousSpeechAgentSpec(GenericAgentSpec):
    speech_llm: Reference(OpenAiSpeech, default=OpenAiSpeech)


class AutonomousSpeechAgent(GenericAgent, Specable[AutonomousSpeechAgentSpec]):
    speech_llm: OpenAiSpeech

    def __init__(self, spec: AutonomousSpeechAgentSpec):
        super().__init__(spec=spec)
        self.speech_llm = self.spec.speech_llm.instantiate()

    @register_program()
    async def speech_question(self, process_id, file: UploadFile = File(...)) -> bytes:
        audio = AudioSegment.from_file(file.file.read())
        # Convert to mp3
        audio_mp3 = audio.export("audio.mp3", format="mp3")

        text = await self.speech_llm.speech_to_text(audio_mp3)
        result = await super().question(process_id, question=text)
        text_result = result.data.response
        audio_result = await self.speech_llm.text_to_speech(text_result)
        return Response(content=audio_result, media_type=audio.content_type)
