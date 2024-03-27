from typing import List
from fastapi import Body
from pydantic import BaseModel, Field
from eidolon_ai_sdk.agent.agent import register_program, Agent, AgentState  # Use register_action
from eidolon_ai_sdk.cpu.agent_io import UserTextCPUMessage
from eidolon_ai_sdk.cpu.llm_output import CPUMessageResponse
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
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(p.text for p in soup.find_all('p'))
        model = Summarizer()
        summary = model(text)
        return summary
    except Exception as e:
        return f"Error retrieving or summarizing webpage: {e}"

class RelevanceRanker(Specable[RelevanceRankerSpec]):
    @register_program()
    async def summarize_websites(self, process_id, input: UrlInput = Body(...)) -> AgentState[CompanySummaries]:
        summaries = []
        for url in input.urls:
            summary_text = scrape_and_summarize(url)
            prompt = f"""
            Given the investment thesis: '{input.investment_thesis}', evaluate the relevance of the following company summary:

            Company Summary:
            {summary_text}

            Determine if the company is directly related to the industry mentioned in the investment thesis, somewhat related, or unrelated. Provide the relevance as 'high' if directly related, 'medium' if somewhat related, or 'low' if unrelated. Only respond with the relevance score (high, medium, or low).
            """
            
            main_thread = await self.cpu.main_thread(process_id)
            llm_message = UserTextCPUMessage(prompt=prompt.strip())
            relevance_evaluation = "low"  # Default value

            async for event in main_thread.stream_request(prompts=[llm_message], output_format=CPUMessageResponse):
                if event.response:  # Check if there's a valid response
                    relevance_evaluation = event.response.strip().lower()
                    if relevance_evaluation not in ["low", "medium", "high"]:
                        relevance_evaluation = "low"  # Validate and normalize the response
                    break  # Assuming we take the first valid response
            
            summaries.append(CompanySummary(url=url, summary=summary_text, relevance=relevance_evaluation))
        
        return AgentState(name="idle", data=CompanySummaries(summaries=summaries))