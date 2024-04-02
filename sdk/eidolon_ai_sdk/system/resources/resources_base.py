from __future__ import annotations

import os
from typing import List, Literal, Optional, TypeVar, Type, Dict

import yaml
from pydantic import BaseModel

from eidolon_ai_client.util.logger import logger


class Metadata(BaseModel):
    name: str = "DEFAULT"
    annotations: List[Dict[str, str]] = []
    labels: List[str] = []


T = TypeVar("T", bound=BaseModel)


class Resource(BaseModel, extra="allow"):
    apiVersion: Literal["eidolon/v1"]
    kind: str
    metadata: Metadata = Metadata()

    @classmethod
    def kind_literal(cls) -> Optional[str]:
        return getattr(cls.model_fields["kind"].annotation, "__args__", [None])[0]

    def promote(self, clazz: Type[T]) -> T:
        return clazz.model_validate(self.model_dump())


def load_resources(path):
    logger.debug(f"Loading resources from {os.path.abspath(path)}")
    if not os.path.exists(path):
        raise ValueError(f"Path {path} does not exist")
    if os.path.isfile(path):
        yield from _load_resources_from_file(path)
    else:
        for file_loc in (os.path.join(p, f) for p, _, files in os.walk(path) for f in files):
            try:
                if file_loc.endswith(".yaml"):
                    yield from _load_resources_from_file(file_loc)
                else:
                    logger.info(f"Skipping {file_loc}")
            except Exception as e:
                raise ValueError(f"Error building resource {file_loc}") from e


def _load_resources_from_file(file_loc):
    with open(file_loc) as resource_yaml:
        for loaded in yaml.safe_load_all(resource_yaml):
            if loaded:
                yield Resource.model_validate(loaded), file_loc
