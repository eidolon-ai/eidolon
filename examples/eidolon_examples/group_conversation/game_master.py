from fastapi import Body
from pydantic import BaseModel, Field
from typing import List, Annotated

from eidolon_examples.group_conversation.base_conversation_coordinator import (
    BaseConversationCoordinator,
    BaseConversationCoordinatorSpec,
    StartConversation,
)
from eidolon_ai_sdk.agent.agent import register_program, AgentState, register_action
from eidolon_ai_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage
from eidolon_ai_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_client.events import AgentStateEvent
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.util.stream_collector import StringStreamCollector


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
        self.cpu.logic_units.append(PlayerLogicUnit(game_master=self, processing_unit_locator=self.cpu, spec={}))

    @register_program()
    async def start_game(
        self, process_id, game: Annotated[str, Body(description="The topic of the new conversation", embed=True)]
    ):
        """
        Called to start the game. Initializes the remote agents and starts the first turn.
        """
        t = await self.cpu.main_thread(process_id)
        system_prompt = f"{self.spec.system_prompt}\n\nYou are playing the game {game}\n You must always remember the rules of the game and follow them"
        await t.set_boot_messages(prompts=[SystemCPUMessage(prompt=system_prompt)])
        message = f"Find the rules of {game} and summarize them. Make sure to include all the rules in detail.\n"
        collector = StringStreamCollector()
        async for event in t.stream_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str):
            collector.process_event(event)
            yield event

        # start conversation with every agent
        async for event in self.start_conversations(
            process_id,
            StartConversation(message=f"Let's play {game}!", max_num_concurrent_conversations=len(self.spec.agents)),
        ):
            yield event

        system_prompt = (
            f"{self.spec.system_prompt}\n\nYou are playing the game {game}\n You must always remember the rules of the game and follow them\n"
            f"You are playing a game with {self.spec.agents}"
        )
        await t.set_boot_messages(prompts=[SystemCPUMessage(prompt=system_prompt)])
        message = "Tell all agents the rules of the game\n"
        async for event in t.stream_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str):
            yield event

        message = "Have the agents introduce themselves and let's start the game!"
        async for event in t.stream_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str):
            yield event

        yield AgentStateEvent(state="take_turn")

    @register_action("take_turn")
    async def take_turn(self, process_id):
        """
        Called to allow the agent to speak
        """
        message = "Play the next turn of the game.\n"
        t = await self.cpu.main_thread(process_id)
        async for event in t.stream_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str):
            yield event
        yield AgentStateEvent(state="take_turn")

    @register_action("take_turn")
    async def speak_to_game_master(
        self, process_id, message: Annotated[str, Body(description="The message to send to the game master", embed=True)]
    ) -> AgentState[str]:
        """
        Called to allow the agent to speak
        """
        t = await self.cpu.main_thread(process_id)
        async for event in t.stream_request(prompts=[UserTextCPUMessage(prompt=message)], output_format=str):
            yield event
        yield AgentStateEvent(state="take_turn")


class PlayerLogicUnit(LogicUnit):
    def __init__(self, game_master: GameMaster, **kwargs):
        super().__init__(**kwargs)
        self.game_master = game_master
        self.game_master_name = game_master.spec.agent_name

    @llm_function()
    async def say_to_players(
        self, statement: PlayerStatement = Field(description="The players and statement you want to talk to")
    ):
        """
        Say something to players. Other players will hear this message and the responses from all other players.
        """
        process_id = RequestContext.get("process_id")
        return self.game_master.speak_to_agents(process_id, f"{self.game_master_name}: {statement}")

    @llm_function()
    async def whisper_to_player(
        self,
        player_name: str = Field(description="Player to whisper to"),
        message: str = Field(description="The message to whisper"),
    ):
        """
        Whisper something to only one player. This is a private message, other players will not hear this message. You can only whisper one player at a time.
        """
        process_id = RequestContext.get("process_id")
        message = f"{self.game_master_name} (whispering only to you): {message}"
        return self.game_master.speak_to_agents(process_id, message, [player_name], should_record=False)

    @llm_function()
    async def say_to_player(
        self,
        player_name: str = Field(description="Player to talke to"),
        message: str = Field(description="The message to say to the player"),
    ):
        """
        Say something to only one player. Other players will hear this message.
        """
        process_id = RequestContext.get("process_id")
        message = f"{self.game_master_name} (whispering only to you): {message}"
        return self.game_master.speak_to_agents(process_id, message, [player_name])

    @llm_function()
    async def speak_amongst_group(
        self,
        players: List[str] = Field(description="The group of players (or agents) that will speak and hear all messages"),
        message: str = Field(description="The message to say to the players"),
    ):
        """
        Called to have a group of agents speak amongst themselves.
        """
        process_id = RequestContext.get("process_id")
        return self.game_master.speak_to_agents(process_id, message, players)
