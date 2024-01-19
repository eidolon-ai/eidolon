from fastapi import Body
from pydantic import BaseModel, Field
from typing import List, Annotated, Tuple

from eidolon_examples.group_conversation.base_conversation_coordinator import BaseConversationCoordinator, BaseConversationCoordinatorSpec, StartConversation
from eidolon_examples.group_conversation.conversation_agent import SpeakResult
from eidos_sdk.agent.agent import register_program, AgentState, register_action
from eidos_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage
from eidos_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidos_sdk.system.reference_model import Specable, AnnotatedReference
from eidos_sdk.system.request_context import RequestContext


class PlayerStatement(BaseModel):
    players: List[str] = Field(description="The players you want to talk to")
    statement: str = Field(description="The statement you want to say to the players")


class RoleResponse(BaseModel):
    agent_name: str
    role: str
    role_description: str


class GameMasterSpec(BaseConversationCoordinatorSpec):
    cpu: AnnotatedReference[ConversationalAgentCPU]
    system_prompt: str
    agent_name: str


class GameMaster(BaseConversationCoordinator, Specable[GameMasterSpec]):
    cpu: ConversationalAgentCPU

    def __init__(self, **kwargs):
        super().__init__("game", **kwargs)
        self.cpu = self.spec.cpu.instantiate()
        self.cpu.logic_units.append(PlayerLogicUnit(game_master=self, processing_unit_locator=self.cpu))

    @register_program()
    async def start_game(self, process_id, game: Annotated[str, Body(description="The topic of the new conversation", embed=True)]) -> AgentState[str]:
        """
        Called to start the game. Initializes the remote agents and starts the first turn.
        """
        # start conversation with every agent
        await self.start_conversations(process_id, StartConversation(message=f"Let's play {game}!", max_num_concurrent_conversations=len(self.spec.agents)))

        t = await self.cpu.main_thread(process_id)
        system_prompt = f"{self.spec.system_prompt}\n\nYou are playing a game with {self.spec.agents}"
        await t.set_boot_messages(prompts=[SystemCPUMessage(prompt=system_prompt)])
        response = ""
        message = f"Find the rules of {game} and summarize them. Make sure to include all the rules in detail.\n"
        response += await t.run_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str)

        message = "Tell every agent the rules of the game\n"
        response += await t.run_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str)

        message = "Have the agents introduce themselves and let's start the game!"
        response += await t.run_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str)

        return AgentState(name="take_turn", data=response)

    @register_action("take_turn")
    async def take_turn(self, process_id) -> AgentState[str]:
        """
        Called to allow the agent to speak
        """
        message = "Play the next turn of the game.\n"
        t = await self.cpu.main_thread(process_id)
        response = await t.run_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str)
        return AgentState(name="take_turn", data=response)

    @register_action("take_turn")
    async def speak_to_game_master(self, process_id, message: Annotated[str, Body(description="The message to send to the game master", embed=True)]) -> AgentState[str]:
        """
        Called to allow the agent to speak
        """
        t = await self.cpu.main_thread(process_id)
        response = await t.run_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str)
        return AgentState(name="take_turn", data=response)


class PlayerLogicUnit(LogicUnit):
    def __init__(self, game_master: GameMaster, **kwargs):
        super().__init__(**kwargs)
        self.game_master = game_master
        self.game_master_name = game_master.spec.agent_name

    @llm_function()
    async def say_to_players(self, statement: PlayerStatement = Field(description="The players and statement you want to talk to")) -> List[Tuple[str, SpeakResult]]:
        """
        Say something to players. Other players will hear this message and the responses from all other players.
        """
        process_id = RequestContext.get("process_id")
        return await self.game_master.speak_to_agents(process_id, f"{self.game_master_name}: {statement}")

    @llm_function()
    async def whisper_to_player(self,
                                player_name: str = Field(description="Player to whisper to"),
                                message: str = Field(description="The message to whisper")) -> Tuple[str, SpeakResult]:
        """
        Whisper something to only one player. This is a private message, other players will not hear this message. You can only whisper one player at a time.
        """
        process_id = RequestContext.get("process_id")
        message = f"{self.game_master_name} (whispering only to you): {message}"
        result = await self.game_master.speak_to_agents(process_id, message, [player_name], should_record=False)

        return result[0]

    @llm_function()
    async def say_to_player(self,
                            player_name: str = Field(description="Player to talke to"),
                            message: str = Field(description="The message to say to the player")) -> Tuple[str, SpeakResult]:
        """
        Say something to only one player. Other players will hear this message.
        """
        process_id = RequestContext.get("process_id")
        message = f"{self.game_master_name} (whispering only to you): {message}"
        result = await self.game_master.speak_to_agents(process_id, message, [player_name])

        return result[0]

    @llm_function()
    async def speak_amongst_group(self, players: List[str] = Field(description="The group of players (or agents) that will speak and hear all messages"),
                                  message: str = Field(description="The message to say to the players")) -> List[Tuple[str, SpeakResult]]:
        """
        Called to have a group of agents speak amongst themselves.
        """
        process_id = RequestContext.get("process_id")
        result = await self.game_master.speak_to_agents(process_id, message, players)

        return result
