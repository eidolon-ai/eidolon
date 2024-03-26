import requests
from bs4 import BeautifulSoup
from summarizer import Summarizer

def scrape_and_summarize(url):
    # Scrape the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the text
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))

    # Summarize the text
    model = Summarizer()
    summary = model(text)

    return summary

# Example usage:
url = "https://droplette.io/"
summary = scrape_and_summarize(url)
print(summary)

