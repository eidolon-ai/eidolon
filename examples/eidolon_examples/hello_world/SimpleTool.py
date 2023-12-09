from eidos.cpu.logic_unit import llm_function, LogicUnit


class MathsTool(LogicUnit):
    """
    A simple tool that performs basic math operations.
    """
    @llm_function
    def add(self, a, b):
        """
        Adds two numbers together.
        :param a: The first number
        :param b: The second number
        :return: The result of adding a and b
        """
        return a + b

    @llm_function
    def subtract(self, a, b):
        """
        Subtracts b from a.
        :param a: The first number
        :param b: The second number
        :return: The result of subtracting b from a
        """
        return a - b

    @llm_function
    def multiply(self, a, b):
        """
        Multiplies two numbers together.
        :param a: The first number
        :param b: The second number
        :return: The result of multiplying a and b
        """
        return a * b

    @llm_function
    def divide(self, a, b):
        """
        Divides a by b.
        :param a: The first number
        :param b: The second number
        :return: The result of dividing a by b
        """
        return a / b
