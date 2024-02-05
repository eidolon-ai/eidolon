from typing import TypeVar, Generic

from pydantic import BaseModel

from eidos_sdk.system.reference_model import Specable


T = TypeVar("T", bound=BaseModel)


class ConfigWrapper(Generic[T], Specable[T]):
    def __getitem__(self, item):
        return self.spec[item]
