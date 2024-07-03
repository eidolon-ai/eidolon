import hashlib
import json
from pathlib import Path

from anthropic import BaseModel


class TestCase(BaseModel):
    db_id: str
    question: str
    query: str

    def identifier(self):
        instance_dict = self.model_dump()
        input_string = json.dumps(instance_dict, sort_keys=True)
        return hashlib.md5(input_string.encode()).hexdigest()


def load_testcases(dbs_loc: Path) -> list[TestCase]:
    with open(dbs_loc, "r") as f:
        return [TestCase(**db) for db in json.load(f)]
