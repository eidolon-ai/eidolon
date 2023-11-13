from eidolon_sdk.agent import CodeAgent, register


class HelloWorld(CodeAgent):
    @register(transition_to=['idle'])
    async def execute(self, name: str):
        return {
            "welcome_message": f'Hello, World {name}!'
        }
