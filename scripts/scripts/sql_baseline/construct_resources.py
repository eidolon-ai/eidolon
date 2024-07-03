from pathlib import Path
from typing import List

import yaml

from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from scripts.sql_baseline.dev_dp import TestCase


def sqlagent(db_loc: Path, name: str):
    db_loc = str(db_loc / name / f'{name}.sqlite')
    if not Path(db_loc).exists():
        raise FileNotFoundError(f"Database file not found: {db_loc}")
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=name),
        spec=dict(
            implementation="SqlAgent",
            client=dict(connection_string=f"sqlite+aiosqlite:///{db_loc}")
        )
    )


def build_resources(db_loc: Path, devdb: List[TestCase], write_loc: Path):
    for db_id in {db.db_id for db in devdb}:
        try:
            resource = sqlagent(db_loc, db_id)
            with open(Path(write_loc) / f"{resource.metadata.name}.yaml", "w") as f:
                yaml.dump(resource.model_dump(), f)
        except FileNotFoundError as e:
            print(str(e))

    additional_resources = Path(__file__).parent / "additional_resources"
    for resource in additional_resources.iterdir():
        with open(additional_resources / resource, "r") as read:
            content = read.read()
        resource_filename = Path(resource).name
        with open(Path(write_loc) / resource_filename, "w") as write:
            write.write(content)
