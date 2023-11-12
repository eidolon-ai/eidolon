from __future__ import annotations

from typing import Dict, Callable


class Agent:
    # todo, we can grab state mappings and default state nicely using annotations
    # todo, we need a constructor here which gives users access to system interfaces off of this object
    starting_state: str
    state_mapping: Dict[str, Callable]


class CodeAgent(Agent):
    pass
