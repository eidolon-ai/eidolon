from abc import ABC
from fastapi import Request
from fastapi.openapi.models import Response


class IOUnit:
    @staticmethod
    def read(self, request: Request):
        pass

    @staticmethod
    def write(data, response: Response):
        pass


class LogicUnit:
    @staticmethod
    def execute(instruction):
        pass


class MemoryUnit:
    @staticmethod
    def load(address):
        pass

    @staticmethod
    def store(address, data):
        pass


class ControlUnit(ABC):
    @staticmethod
    def fetch(self):
        pass

    @staticmethod
    def decode(instruction):
        pass

    @staticmethod
    def execute(decoded_instruction):
        pass


class LLMUnit:
    @staticmethod
    def query(prompt):
        pass

    @staticmethod
    def respond(prompt):
        pass
