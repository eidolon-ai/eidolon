from typing import List
from fastapi import Body
from pydantic import BaseModel, Field
from eidolon_ai_sdk.agent.agent import register_program, Agent, AgentState
from eidolon_ai_sdk.cpu.agent_io import UserTextCPUMessage
import requests
from bs4 import BeautifulSoup
from summarizer import Summarizer

class UrlInput(BaseModel):
    urls: List[str] = Field(..., description="List of URLs to scrape and summarize")
    investment_thesis: str = Field(..., description="Investment thesis to match against company summaries")

class CompanySummary(BaseModel):
    url: str
    summary: str
    relevance: str

class CompanySummaries(BaseModel):
    summaries: List[CompanySummary]

def scrape_and_summarize(url: str) -> str:
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(p.text for p in soup.find_all('p'))
        model = Summarizer()
        summary = model(text)
        return summary
    else:
        return "Error retrieving webpage."

class VenturePortfolioAgent(Agent):
    @register_program()
    async def summarize_websites(self, process_id, input: UrlInput = Body(...)) -> AgentState[CompanySummaries]:
        summaries = []
        for url in input.urls:
            summary_text = scrape_and_summarize(url)
            prompt = f"""
            Given the investment thesis: '{input.investment_thesis}', evaluate the relevance of the following company summary to the health industry:

            Company Summary:
            {summary_text}

            Determine if the company is directly related to health, somewhat related, or unrelated. Provide the relevance as 'high' if directly related, 'medium' if somewhat related, or 'low' if unrelated. Only respond with the relevance score (high, medium, or low).
            """
            
            # Obtain the main thread of the agent's CPU
            main_thread = await self.cpu.main_thread(process_id)
            
            # Create a message for LLM interaction, wrapped in UserTextCPUMessage
            llm_message = UserTextCPUMessage(prompt=prompt.strip())
            
            # Send the message through the main thread and wait for the response
            async for event in main_thread.stream_request(prompts=[llm_message], output_format=str):
                relevance_evaluation = event.strip().lower()
            
            # Validate and normalize the relevance evaluation
            if relevance_evaluation not in ["low", "medium", "high"]:
                relevance_evaluation = "low"  # Default to low if the response is not valid
            
            summaries.append(CompanySummary(url=url, summary=summary_text, relevance=relevance_evaluation))
        
        return AgentState(name="idle", data=CompanySummaries(summaries=summaries))





