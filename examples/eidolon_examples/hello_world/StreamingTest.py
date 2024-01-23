from typing import Annotated

from fastapi import Body

from eidos_sdk.agent.agent import register_program, register_action
from eidos_sdk.io.events import StringOutputEvent, AgentStateEvent, StartLLMEvent, EndLLMEvent, ObjectOutputEvent


class StreamingTest:
    @register_program()
    async def streaming(self, name: Annotated[str, Body(embed=True)]):
        yield StartLLMEvent(stream_context=["foo"])
        yield StringOutputEvent(stream_context=["foo"], content="Hello,")
        yield StringOutputEvent(stream_context=["foo"], content=f"{name}")
        yield StringOutputEvent(stream_context=["foo"], content="!")
        yield AgentStateEvent(stream_context=["foo"], state="terminated")
        yield EndLLMEvent(stream_context=["foo"])

    @register_program()
    @register_action("idle")
    async def streaming_object(self, name: Annotated[str, Body(embed=True)]):
        yield ObjectOutputEvent(stream_context=["foo"], content={"hello": f"{name}"})
        yield AgentStateEvent(stream_context=["foo"], state="idle")
