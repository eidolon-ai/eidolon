from fastapi import Body
from jinja2 import Environment, StrictUndefined
import pyodbc
from typing import Dict
import os 

from eidolon_ai_sdk.agent.agent import Agent, AgentSpec, register_program
from eidolon_ai_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidolon_ai_sdk.system.reference_model import Specable
# from eidolon_ai_sdk.util.logger import logger


class SqlAgentSpec(AgentSpec):
    system_prompt: str
    user_prompt: str
    extra_template_args: dict = {}


class SqlAgent(Agent, Specable[SqlAgentSpec]):
    @register_program()
    async def execute(self, process_id, query: str = Body()):
        """
        execute sql query from natural language
        :param process_id:
        :param query:
        :return:
        """
        env = Environment(undefined=StrictUndefined)
        system_prompt = env.from_string(self.spec.system_prompt).render(query=query, **self.spec.extra_template_args)
        user_prompt = env.from_string(self.spec.user_prompt).render(query=query, **self.spec.extra_template_args)

        llm_thread = await self.cpu.main_thread(process_id)
        response_text = await llm_thread.run_request(
            [SystemCPUMessage(prompt=system_prompt), UserTextCPUMessage(prompt=user_prompt)]
        )
        response_text = response_text.replace("```SQL", "").replace("```", "").strip()
        start_idx = response_text.find("SELECT")
        sql_statement = response_text[start_idx:] if start_idx != -1 else response_text
        sql_statement = sql_statement.rstrip(';').strip()
        # logger.info(sql_statement)
#         todo actually execute sql
        return sql_query(sql_statement)

def sql_query(sql_statement: str) -> Dict:
    # Updated connection string with new database details
    conn_str = os.environ.get("CRIME_SQL_CONNECTION_STRING")
    
    # try:
    #     # Establish a connection to the database
    with pyodbc.connect(conn_str) as conn:
        print("Connected Successfully")
        # Create a cursor from the connection
        cursor = conn.cursor()
        
        # Execute the provided SQL statement
        cursor.execute(sql_statement)
        
        # Fetch all the results
        results = cursor.fetchall()
        
        # Assuming you want to return the results as a list of dictionaries
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in results]
            
    # except pyodbc.Error as e:
    #     print("An error occurred:", e)
    #     # return {}  # Return an empty dictionary or handle the error as appropriate

# # Example usage:
# sql_statement = "SELECT TOP 10 * FROM IncidentReports"  # Replace with your actual SQL query
# results = sql_query(sql_statement)
# for row in results:
#     print(row)
