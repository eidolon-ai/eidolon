from typing import List, Dict
from fastapi import Body
from pydantic import BaseModel, Field
from eidolon_ai_sdk.agent.agent import register_program
import requests
from bs4 import BeautifulSoup
from summarizer import Summarizer

# Define a model for the input URLs
class UrlInput(BaseModel):
    urls: List[str] = Field(..., description="List of URLs to scrape and summarize")

# Define a model for the output summaries
class CompanySummary(BaseModel):
    url: str
    summary: str

class CompanySummaries(BaseModel):
    summaries: List[CompanySummary]

# Summarization function
def scrape_and_summarize(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(p.text for p in soup.find_all('p'))
    model = Summarizer()
    summary = model(text)
    return summary

class VenturePortfolioAgent:
    @register_program()
    async def summarize_websites(self, urls: UrlInput = Body(...)) -> CompanySummaries:
        summaries = []
        for url in urls.urls:
            summary_text = scrape_and_summarize(url)
            summaries.append(CompanySummary(url=url, summary=summary_text))
        return CompanySummaries(summaries=summaries)


