from typing import Annotated

from pydantic import Field

from eidolon_sdk.agent import CodeAgent, register


class HelloWorld(CodeAgent):
    @register(state='idle', transition_to=['idle'])
    async def execute(self, name: Annotated[str, Field(description="Your name")]) -> dict:
        return {
            "welcome_message": f'Hello, World {name}!'
        }
