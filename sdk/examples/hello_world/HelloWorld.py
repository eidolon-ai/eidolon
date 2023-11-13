from typing import Dict, Any

from eidolon_sdk.agent import CodeAgent


class HelloWorld(CodeAgent):
    async def execute(self, state_name: str, input: Dict[str, Any]):
        return {
            "welcome_message": f'Hello, World {input["name"]}!'
        }
