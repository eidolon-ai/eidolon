from eidos_sdk.cpu.logic_unit import llm_function, LogicUnit


class MathsTool(LogicUnit):
    """
    A simple tool that performs basic math operations.
    """

    @llm_function()
    async def add(self, a: float, b: float) -> float:
        """
        Adds two numbers together.
        :param a: The first number
        :param b: The second number
        :return: The result of adding a and b
        """
        return a + b

    @llm_function()
    async def subtract(self, a: float, b: float) -> float:
        """
        Subtracts b from a.
        :param a: The first number
        :param b: The second number
        :return: The result of subtracting b from a
        """
        return a - b

    @llm_function()
    async def multiply(self, a: float, b: float) -> float:
        """
        Multiplies two numbers together.
        :param a: The first number
        :param b: The second number
        :return: The result of multiplying a and b
        """
        return a * b

    @llm_function()
    async def divide(self, a: float, b: float) -> float:
        """
        Divides a by b.
        :param a: The first number
        :param b: The second number
        :return: The result of dividing a by b
        """
        return a / b
