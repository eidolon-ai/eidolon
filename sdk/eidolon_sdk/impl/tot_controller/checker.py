from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from eidolon_sdk.impl.tot_controller.thought import ThoughtValidity


class ToTChecker(ABC):
    """
    Tree of Thought (ToT) checker.

    This is an abstract ToT checker that must be implemented by the user. You
    can implement a simple rule-based checker or a more sophisticated
    neural network based classifier.
    """

    output_key: str = "validity"  #: :meta private:

    @property
    def input_keys(self) -> List[str]:
        """The checker input keys.

        :meta private:
        """
        return ["problem_description", "thoughts"]

    @property
    def output_keys(self) -> List[str]:
        """The checker output keys.

        :meta private:
        """
        return [self.output_key]

    @abstractmethod
    def evaluate(
        self,
        problem_description: str,
        thoughts: Tuple[str, ...] = (),
    ) -> ThoughtValidity:
        """
        Evaluate the response to the problem description and return the solution type.
        """

    def _call(
        self,
        inputs: Dict[str, Any],
    ) -> Dict[str, ThoughtValidity]:
        return {self.output_key: self.evaluate(**inputs)}
