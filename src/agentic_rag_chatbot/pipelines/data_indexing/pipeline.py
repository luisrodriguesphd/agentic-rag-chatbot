"""
Data Indexing Pipeline

Indexing is the process of organizing data in a way that makes it more efficient to retrieve information later.

This pipeline indexes the job vacancy files on a library compose by a vector database and a embedding model.
"""


import os
import pandas as pd

from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.pipelines.data_indexing.nodes import extract_and_parse_webpages, clean_webpage_text, index_documents


params = get_params()
embedding_dir = params['embedding_dir']
embedding_model = params['embedding_model']


def extract_parse_and_index_webpages(data_dir: list[str], ingestion_metadata_file: str, min_page_length: int = 200):

    # Stage 1 - Get webpages to ingest 
    
    file_path = os.path.join(data_dir, ingestion_metadata_file)
    webpage_ingestion_control = pd.read_csv(file_path)
    urls = list(webpage_ingestion_control[webpage_ingestion_control.is_to_ingest]['url'].values)

    # Stage 2 - Extract and parse webpages
    
    docs = extract_and_parse_webpages(urls)

    # Stage 3 - Clean up the webpage content

    docs_clean = []
    for doc in docs:
        raw_text = doc.page_content
        clean_text = clean_webpage_text(raw_text)
        if len(clean_text) > min_page_length:
            doc.page_content = clean_text
            docs_clean.append(doc)

    # Stage 4 - Embedd and index documents

    vectordb = index_documents(docs_clean, embedding_dir, embedding_model)

    print(f"-> Indexed {vectordb._collection.count()} documents")

    return vectordb


if __name__ == "__main__":

    # Get parameters

    params = get_params()
    data_dir = params['data_dir']
    ingestion_metadata_file = params['ingestion_metadata_file']

    # Run pipeline

    extract_parse_and_index_webpages(data_dir, ingestion_metadata_file)
