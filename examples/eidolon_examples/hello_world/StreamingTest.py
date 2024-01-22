from typing import Annotated

from fastapi import Body

from eidos_sdk.agent.agent import register_program
from eidos_sdk.io.events import StartStreamEvent, EndStreamEvent, StopReason, StringOutputEvent, AgentStateEvent


class StreamingTest:
    @register_program()
    async def streaming(self, name: Annotated[str, Body(embed=True)]):
        yield StartStreamEvent(stream_context=["foo"])
        yield StringOutputEvent(stream_context=["foo"], content="Hello,")
        yield StringOutputEvent(stream_context=["foo"], content=f"{name}")
        yield StringOutputEvent(stream_context=["foo"], content="!")
        yield AgentStateEvent(stream_context=["foo"], state="terminated")
        yield EndStreamEvent(stream_context=["foo"], stop_reason=StopReason.COMPLETED)
