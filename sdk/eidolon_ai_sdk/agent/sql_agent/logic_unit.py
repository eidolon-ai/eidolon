from eidolon_ai_sdk.agent.sql_agent.client import SqlClient
from eidolon_ai_sdk.apu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnitLocator


class SqlLogicUnit(LogicUnit):
    def __init__(self, client: SqlClient, apu: ProcessingUnitLocator):
        super().__init__(apu)
        self.client = client

    @llm_function()
    async def peek(self, query: str, row_limit: int = 10) -> dict:
        """
        Execute a query and see return the first few rows of a query.
        """
        rows = []
        async for row in self.client.execute(query):
            rows.append(row)
            if len(rows) >= row_limit:
                break

        return dict(rows=rows)
