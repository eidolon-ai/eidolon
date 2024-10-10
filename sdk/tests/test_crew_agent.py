from datetime import time
from time import perf_counter

import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.crew.crew_agent import CrewAgent
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn

resources = [
    Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name="example_crew"),
        spec=dict(
            implementation=fqn(CrewAgent),
            agents=dict(researcher={
                "role": "Senior Researcher",
                "goal": "Uncover groundbreaking technologies in AI",
                "backstory": "Driven by curiosity, you explore and share the latest innovations."
            }),
            tasks=dict(trendfinder={
                "description": "Identify the next big trend in AI with pros and cons.",
                "expected_output": "A 3-paragraph report on emerging AI technologies.",
                "agent": "researcher",
            }),
            crew=dict(
                memory=True,
            )
        ),
    )
]


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(*resources) as ra:
        yield ra


@pytest.fixture()
def agent():
    return Agent.get("example_crew")


async def test_default_agent(agent):
    process = await agent.create_process()

    t0 = perf_counter()
    await process.action("kickoff", body={"topic": "AI in healthcare"})
    print(f"elapsed time: {perf_counter()-t0}s")
