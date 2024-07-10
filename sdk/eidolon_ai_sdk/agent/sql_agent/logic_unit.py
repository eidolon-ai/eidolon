from eidolon_ai_sdk.agent.sql_agent.client import SqlClient
from eidolon_ai_sdk.apu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnitLocator


class SqlLogicUnit(LogicUnit):
    def __init__(self, client: SqlClient, apu: ProcessingUnitLocator):
        super().__init__(apu)
        self.client = client

    @llm_function()
    async def research(self, query: str) -> dict:
        """
        Execute a query against the sql db.
        """
        rows = []
        async for row in self.client.execute(query):
            rows.append(row)

        return dict(first_10_rows=rows[:10], num_rows=len(rows))
