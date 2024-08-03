import re

from datetime import date
from langchain_community.document_loaders import WebBaseLoader
from langchain.docstore.document import Document


def extract_and_parse_webpages(webpage_urls: str) -> list[Document]:
    """Extract webpages and parse as LangChain's Documents"""

    loader = WebBaseLoader(webpage_urls)
    loader.requests_per_second = 50
    loader.continue_on_failure = True

    docs = loader.aload()

    return docs


def clean_webpage_text(text: str):
    """Clean up the webpage content by removing unnecessary whitespaces, newlines, 
    and non-printable characters like \xa0."""

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-printable characters like \xa0
    text = re.sub(r'\xa0', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def parse_ingested_web_data(urls_qualified, urls_disqualified):
    # Get today's date and format the date as YYYY-MM-DD
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    urls = urls_qualified + urls_disqualified
    is_to_ingest = [False for url in urls]
    ingestion_date = [today_str for url in urls]
    ingested_successfully = [True if url in urls_qualified else False for url in urls]

    web_data_to_update = []
    for url, ii, id, isuc in  zip(urls, is_to_ingest, ingestion_date, ingested_successfully):
        data = {
            'url': url,
            'is_to_ingest': ii,
            'ingestion_date': id,
            'ingested_successfully': isuc,
        }
        web_data_to_update.append(data)

    return web_data_to_update
