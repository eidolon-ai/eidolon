import asyncio
import json
import os
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Literal

import typer
from pydantic import BaseModel, computed_field
from rich.console import Console
from rich.style import Style
from sqlalchemy import text
from sqlalchemy.dialects import sqlite

from eidolon_ai_client.client import Agent
from eidolon_ai_client.events import BaseStreamEvent, ObjectOutputEvent, OutputEvent
from eidolon_ai_sdk.agent.sql_agent.client import SqlAlchemy
from scripts.sql_baseline.construct_resources import build_resources
from scripts.sql_baseline.dev_dp import load_testcases, TestCase

app = typer.Typer()
console = Console()
dim_console = Console(style=Style(dim=True))
warning_console = Console(stderr=True, style="dark_orange3")
err_console = Console(stderr=True, style="red")


class ResourcesMetadata(BaseModel):
    testcases: Path
    databases: Path
    total_testcases: int
    apu_override: Optional[str] = None
    run_testcases: int = 0
    sql_match: int = 0
    data_match: int = 0
    better_or_equal_query: int = 0
    strictly_better: int = 0
    strictly_worse_scenarios: List[str] = []
    extra: dict = {}

    @computed_field
    @property
    def sql_match_rate(self) -> float:
        if self.run_testcases == 0:
            return 0
        return self.sql_match / self.run_testcases * 100

    @computed_field
    @property
    def data_match_rate(self) -> float:
        if self.run_testcases == 0:
            return 0
        return self.data_match / self.run_testcases * 100

    @computed_field
    @property
    def better_query_rate(self) -> float:
        if self.run_testcases == 0:
            return 0
        return self.better_or_equal_query / self.run_testcases * 100

    @computed_field
    @property
    def strictly_worse(self) -> int:
        return self.run_testcases - self.better_or_equal_query

    @computed_field
    @property
    def outperform_rate(self) -> float:
        if self.strictly_better == 0 and self.strictly_worse == 0:
            return -1.0
        return self.strictly_better / (self.strictly_better + self.strictly_worse) * 100


@app.command()
def create_resources(testcases: Path, databases: Optional[Path] = None,
                     write_loc: Path = Path("dist") / "sql_baseline", apu: str = None, allow_thought: bool = None):
    print("Creating resources...")
    resources_loc = write_loc / "resources"
    testcases = testcases.expanduser()
    if os.path.exists(write_loc):
        shutil.rmtree(write_loc)
    os.makedirs(write_loc)
    os.makedirs(resources_loc)

    print(f"Reading from: {testcases}")
    dbs = load_testcases(testcases)
    if not databases:
        if "spider" not in str(testcases):
            raise ValueError("Must provide db_loc if not in spider directory")
        spider_loc = testcases
        while "spider" in str(spider_loc.parent):
            spider_loc = spider_loc.parent
        databases = spider_loc / "test_database"

    extra = {}
    if apu:
        extra["apu"] = apu
    if allow_thought is not None:
        extra["allow_thought"] = allow_thought
    build_resources(databases, dbs, resources_loc, **extra)
    with open(write_loc / "metadata.json", "w") as f:
        f.write(ResourcesMetadata(
            testcases=testcases,
            databases=databases,
            total_testcases=len(dbs),
            apu_override=apu,
            extra=extra,
        ).model_dump_json(indent=2))


@app.command()
def benchmark(loc: Path = Path("dist") / "sql_baseline", test_case: List[str] = None, recalculate: bool = False, parallel: int = 20, limit: Optional[int] = None, output_loc: Path = None):
    with open(loc / "metadata.json", "r") as f:
        metadata = ResourcesMetadata(**json.load(f))
    read_loc = metadata.testcases
    testcases = load_testcases(read_loc)
    write_loc = loc / "results"
    if not write_loc.exists():
        os.makedirs(write_loc)
    if test_case:
        testcases = [tc for tc in testcases if tc.identifier() in test_case]
    if limit:
        testcases = testcases[:limit]
    try:
        asyncio.run(_benchmark(testcases, write_loc, recalculate, metadata, parallel))
    finally:
        results(loc, output_loc)


@app.command()
def results(loc: Path = Path("dist") / "sql_baseline", write: Path = None):
    results_loc = loc / "results"
    results_: Dict[str, BenchmarkResult] = {}
    for file in results_loc.iterdir():
        with open(file, "r") as f:
            data = json.load(f)
            results_[file.name] = BenchmarkResult(**data)

    with open(loc / "metadata.json", "r") as f:
        metadata = ResourcesMetadata(**json.load(f))
    metadata.run_testcases = len(results_)
    metadata.sql_match = len([r for r in results_.values() if r.query_matches])
    metadata.data_match = len([r for r in results_.values() if r.data_matches])
    metadata.better_or_equal_query = len([r for r in results_.values() if r.comparison in {"better", "equal"}])
    metadata.strictly_better = len([r for r in results_.values() if r.comparison == "better"])
    metadata.strictly_worse_scenarios = [k for k, r in results_.items() if r.comparison == "worse"],
    console.log(metadata.model_dump(exclude={"total_testcases", "testcases", "databases", "failures"}))

    with open(loc / "metadata.json", "w") as f:
        f.write(metadata.model_dump_json(indent=2))
    if write:
        with open(write, "w") as f:
            f.write(metadata.model_dump_json(indent=2, exclude={"testcases", "databases", "total_testcases"}))


async def _benchmark(testcases: List[TestCase], write_loc: Path, recalculate: bool, metadata: ResourcesMetadata, parallel: int):
    print("Benchmarking...")
    running_tasks = set()
    while testcases:
        testcase = testcases.pop()
        if len(running_tasks) >= parallel:
            done, running_tasks = await asyncio.wait(running_tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                await task
        running_tasks.add(asyncio.create_task(_test(metadata, recalculate, testcase, write_loc)))
    await asyncio.wait(running_tasks)
    print("Done")


async def _test(metadata, recalculate, testcase, write_loc):
    identifier = testcase.identifier()
    if not (write_loc / identifier).exists() or recalculate:
        dim_console.print(f"{identifier}: running...")
        db_loc = metadata.databases / testcase.db_id / f"{testcase.db_id}.sqlite"
        result = await run_benchmark(testcase, db_loc)
        with open(write_loc / identifier, "w") as f:
            f.write(result.model_dump_json(indent=2))
        if 'error' in result.extra:
            err_console.print(f"{identifier} error: {result.extra['error']}")
            console.print(result)


class BenchmarkResult(BaseModel):
    db_id: str
    question: str
    expected_query: str
    query_matches: bool = False
    data_matches: bool = False
    comparison: Literal["worse", "equal", "better"] = "worse"
    extra: dict = {}


def normalize_sql(statement: str):
    # Convert the statement to a string representation
    compiled = text(statement).compile(
        dialect=sqlite.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    return ' '.join(str(compiled).split())


async def run_benchmark(testcase: TestCase, db_loc) -> BenchmarkResult:
    process = await Agent.get(testcase.db_id).create_process()
    output_event: BaseStreamEvent
    result = BenchmarkResult(db_id=testcase.db_id, question=testcase.question, expected_query=testcase.query)
    try:
        actual_rows = []
        output_events = []
        actual_query: Optional[str] = None
        async for output_event in process.stream_action("query", dict(message=testcase.question, allow_conversation=False)):
            output_events.append(output_event)
            if isinstance(output_event, ObjectOutputEvent):
                if "response_type" in output_event.content and output_event.content["response_type"] == "execute":
                    actual_query = output_event.content["query"]
                    result.extra['actual_query'] = actual_query
                    if actual_query == testcase.query:
                        result.query_matches = True
                        result.data_matches = True
                        result.comparison = "equal"
                        break
            if output_event.is_root_and_type(OutputEvent):
                actual_rows.append(output_event.content)
        if not actual_query:
            result.extra['output_events'] = [e.model_dump() for e in output_events]
            result.extra['error'] = 'No query was returned'
        elif not result.query_matches:
            expected_rows = []
            async for row in SqlAlchemy(connection_string=f"sqlite+aiosqlite:///{db_loc}").execute(result.expected_query):
                expected_rows.append(row)

            if len(expected_rows) != len(actual_rows):
                result.data_matches = False
                result.extra['data_mismatch'] = f'actual returned different number of rows than expected query (expected {len(expected_rows)} found {len(actual_rows)})'
            else:
                matches = True
                while expected_rows:
                    expected = expected_rows.pop()
                    actual = actual_rows.pop()
                    if not expected == actual:
                        result.data_matches = False
                        result.extra['data_mismatch'] = 'data mismatch between expected and actual query.'
                        result.extra['expected_row'] = expected
                        result.extra['actual_row'] = actual
                        matches = False
                        break
                result.data_matches = matches
            if not result.data_matches:
                results.extra['data'] = dict(
                    expected=expected_rows,
                    actual=actual_rows,
                )

            process = await Agent.get("query_comparer").create_process()
            body = dict(
                question=testcase.question,
                query1=result.expected_query,
                len1=str(len(expected_rows)),
                preview1=str(expected_rows[0:5]),
                query2=result.actual_query,
                len2=str(len(actual_rows)),
                preview2=str(actual_rows[0:5]),
            )
            response = await process.action("compare_queries", body)
            response_data: dict = response.data
            if response_data["better_query"] == "query1":
                result.comparison = "worse"
            elif response_data["better_query"] == "query2":
                result.comparison = "better"
            elif response_data["better_query"] == "equal":
                result.comparison = "equal"
            else:
                err_console.print(f"Invalid response from query comparer: {response_data}")
                raise ValueError(f"Invalid response from query comparer: {response_data}")
    except Exception as e:
        result.extra['error'] = str(e)
    return result


if __name__ == "__main__":
    app()
