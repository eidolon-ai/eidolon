from datetime import datetime
from typing import ClassVar, Any

import bson
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from eidos_sdk.agent_os import AgentOS


class MongoDoc(BaseModel, extra="allow"):
    collection: ClassVar[str]
    created: str = None
    updated: str = None

    @property
    def record_id(self):
        return self._id

    @classmethod
    async def find(cls, **kwargs):
        doc = await AgentOS.symbolic_memory.find_one(cls.collection, **kwargs)
        if doc:
            return cls.model_validate(doc)
        else:
            return None

    @classmethod
    async def create(cls, **data):
        t = datetime.now().isoformat()
        if "created" not in data:
            data["created"] = t
        if "updated" not in data:
            data["updated"] = t
        if "_id" not in data:
            data["_id"] = str(bson.ObjectId())
        doc = cls(**data)
        await AgentOS.symbolic_memory.insert_one(cls.collection, doc.model_dump())
        return doc

    async def update(self, **data):
        data = dict(**data, updated=datetime.now().isoformat())
        query = {"_id": self.record_id, "updated": self.updated}
        try:
            await AgentOS.symbolic_memory.upsert_one(self.collection, query=query, document=data)
        except DuplicateKeyError:
            raise ValueError(f"{self.__class__.__name__} record {self.record_id} has been updated since last read")
        dump = self.model_dump()
        dump.update(**data)
        return self.__class__.model_validate(dump)


class ProcessDoc(MongoDoc):
    collection = "processes"
    metadata: dict = {}
    agent: str
    state: str
    data: Any
