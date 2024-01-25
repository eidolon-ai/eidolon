from fastapi import Body
from typing import Annotated

from eidos_sdk.agent.agent import register_program, register_action
from eidos_sdk.io.events import StringOutputEvent, AgentStateEvent, ObjectOutputEvent


class StreamingTest:
    @register_program()
    async def streaming(self, name: Annotated[str, Body(embed=True)]):
        yield StringOutputEvent(content="Hello,")
        yield StringOutputEvent(content=f"{name}")
        yield StringOutputEvent(content="!")
        yield AgentStateEvent(state="terminated")

    @register_program()
    @register_action("idle")
    async def streaming_object(self, name: Annotated[str, Body(embed=True)]):
        yield ObjectOutputEvent(content={"hello": f"{name}"})
        yield AgentStateEvent(state="idle")
