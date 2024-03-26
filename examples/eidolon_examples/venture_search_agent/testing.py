from typing import List
from fastapi import Body
from pydantic import BaseModel, Field
from eidolon_ai_sdk.agent.agent import register_program
import requests
from bs4 import BeautifulSoup

# Assuming the summarizer is available as before
from summarizer import Summarizer

class UrlInput(BaseModel):
    urls: List[str] = Field(..., description="List of URLs to scrape and summarize")
    investment_thesis: str = Field(..., description="Investment thesis to match against company summaries")

class CompanySummary(BaseModel):
    url: str
    summary: str
    relevance: str  # Field to indicate match with the investment thesis

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

class VenturePortfolioAgent:
    @register_program()
    async def summarize_websites(self, input: UrlInput = Body(...)) -> CompanySummaries:
        summaries = []
        for url in input.urls:
            summary_text = scrape_and_summarize(url)
            # Prepare a prompt for the LLM to evaluate the relevance of the summary to the investment thesis
            prompt = f"Given the investment thesis: '{input.investment_thesis}', evaluate the relevance of the following summary: '{summary_text}'"
            
            # Simulating an LLM call to evaluate relevance. Replace with your actual method to make the LLM query.
            # The actual implementation of this call will depend on the specifics of your SDK and setup.
            # For demonstration purposes, let's assume a placeholder response indicating high relevance.
            relevance_result = "Highly Relevant"  # Placeholder for demonstration purposes.
            
            summaries.append(CompanySummary(url=url, summary=summary_text, relevance=relevance_result))
        
        return CompanySummaries(summaries=summaries)

# Note: The actual implementation for making LLM calls (`self.cpu.llm_query(prompt=prompt)`) should be replaced with the specific method provided by your SDK or setup.




