from typing import List

from eidolon_ai_sdk.agent.tot_agent.memory import ToTDFSMemory
from eidolon_ai_sdk.agent.tot_agent.thought import Thought


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
        validity = "INTERMEDIATE" if next_thought is None else next_thought.validity

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
        elif validity == "INTERMEDIATE" and parent_thought and len(parent_thought.children) >= self.c:
            memory.pop(2)

        return [t.text for t in memory.current_path()]

    def exploration_synopsis(self, memory: ToTDFSMemory) -> dict:
        """
        Return the remaining intermediate paths in the ToT and the number of unexplored branches per thought.

        An intermediate path is remaining if it has not yet been explored to the
        maximum depth and has INTERMEDIATE validity.
        """

        def recurse(path: List[Thought]) -> dict:
            rtn = {}
            unexplored_branch_count = self.c - len(path)
            if unexplored_branch_count > 0:
                rtn["UNEXPLORED_BRANCHES"] = unexplored_branch_count
            for child in path:
                if child.validity != "INVALID":
                    recursed_child = recurse(child.children)
                    if recursed_child:
                        rtn[child.text] = recursed_child
            return rtn

        if not memory.stack:
            return {}
        else:
            return {memory.stack[0].text: recurse(memory.stack[0].children)}
