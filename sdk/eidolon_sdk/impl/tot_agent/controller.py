from typing import Tuple, List

from eidolon_sdk.impl.tot_agent.memory import ToTDFSMemory
from eidolon_sdk.impl.tot_agent.thought import ThoughtValidity


class ToTController:
    """
    Tree of Thought (ToT) controller.

    This is a version of a ToT controller, dubbed in the paper as a "Simple Controller".

    It has one parameter `c` which is the number of children to explore for each
    thought.
    """

    def __init__(self, c: int = 3):
        """
        Initialize the controller.

        Args:
            c: The number of children to explore at each node.
        """
        self.c = c

    def thoughts(self, memory: ToTDFSMemory) -> List[str]:
        next_thought = memory.top()
        parent_thought = memory.top_parent()
        validity = (
            "INTERMEDIATE"
            if next_thought is None
            else next_thought.validity
        )

        # 1 if the current partial solution is invalid, backtrack to the parent
        # thought.
        if validity == "INVALID":
            memory.pop()
            next_thought = memory.top()
            if next_thought and len(next_thought.children) >= self.c:
                memory.pop()

        # 2 if the current partial solution is valid but C children were
        # explored and yet failed to find a final solution, backtrack to the
        # parent thought.
        elif (
            validity == "INTERMEDIATE"
            and parent_thought
            and len(parent_thought.children) >= self.c
        ):
            memory.pop(2)

        return [t.text for t in memory.current_path()]
