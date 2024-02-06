import bson
import logging
from datetime import datetime
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from typing import ClassVar, Any, cast, AsyncIterable, Optional, Dict

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.io.events import StreamEvent


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
    error_info: Optional[Any] = None


async def store_events(agent: str, process_id: str, events: list[StreamEvent]):
    try:
        stored_events = []
        for event_num, event in enumerate(events):
            event_obj: Dict[str, Any] = {
                **event.model_dump(),
                "__process_id": process_id,
                "__agent": agent,
                "__create_time": datetime.now().timestamp(),
                "__event_id": event_num,
            }
            event_obj["category"] = event_obj["category"].value
            if hasattr(event_obj["event_type"], "value"):
                event_obj["event_type"] = event_obj["event_type"].value
            event_obj["category"] = str(event_obj["category"])
            stored_events.append(event_obj)

        await AgentOS.symbolic_memory.insert("process_events", stored_events)
    except Exception as e:
        logging.getLogger("eidolon").exception(f"Error storing events {e}")


async def load_events(agent: str, process_id: str):
    query = {"__agent": agent, "__process_id": process_id}
    order = {"__create_time": 1, "__event_id": 1}
    events = cast(AsyncIterable[dict[str, Any]], AgentOS.symbolic_memory.find("process_events", query, sort=order))

    events_arr = [event async for event in events]
    for event in events_arr:
        del event["_id"]
        del event["__process_id"]
        del event["__create_time"]
        del event["__event_id"]
        del event["__agent"]
        if not event["stream_context"]:
            del event["stream_context"]
    return events_arr
