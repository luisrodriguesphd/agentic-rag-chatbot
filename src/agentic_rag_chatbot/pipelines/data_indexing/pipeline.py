"""
Data Indexing Pipeline

Indexing is the process of organizing data in a way that makes it more efficient to retrieve information later.

This pipeline takes the preprocessed documents, convert it into embeddings and store everything in a vector store.
"""

from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.pipelines.data_indexing.nodes import extract_and_parse_webpages, clean_webpage_text, parse_ingested_web_data
from agentic_rag_chatbot.utils.database import get_urls_to_ingest, update_documents
from agentic_rag_chatbot.utils.embeddings import load_embedding_model
from agentic_rag_chatbot.utils.logging import logger
from agentic_rag_chatbot.utils.vector_store import embed_and_store_documents


params = get_params()
min_length_text = params['data_indexing']['min_length_text']
vector_store_name = params['data_indexing']['vector_store_name']
embedding_dir = params['embedding_dir']
embedding_model = params['embedding_model']


embedding = load_embedding_model(embedding_model['model_provider'], embedding_model['model_name'], embedding_model['model_kwargs'], embedding_model['encode_kwargs'], embedding_model['show_progress'])


def extract_parse_and_index_web_pages():

    logger.info('Indexing Pipeline - Started')

    # Stage 1 - Get web pages URLs to ingest 
    logger.info('Stage 1 - Get web pages URLs to ingest')
    
    urls = get_urls_to_ingest()

    logger.info(f'There are {len(urls)} web pages to process')

    # Stage 2 - Extract and parse web pages
    logger.info('Stage 2 - Extract and parse web pages')
    
    docs = extract_and_parse_webpages(urls)

    logger.info(f'There were extracted and parsed {len(docs)} web pages')

    # Stage 3 - Clean up web page content
    logger.info('Stage 3 - Clean up web page content')

    docs_clean = []
    for doc in docs:
        raw_text = doc.page_content
        clean_text = clean_webpage_text(raw_text)
        doc.page_content = clean_text
        docs_clean.append(doc)

    # Stage 4 - Delete web pages whose content is too short
    logger.info('Stage 4 - Delete web pages whose content is too short')

    urls_qualified = []
    urls_disqualified = []
    docs_qualified = []
    for url, doc in zip(urls, docs_clean):
        if len(doc.page_content) > min_length_text:
            docs_qualified.append(doc)
            urls_qualified.append(url)
        else:
            urls_disqualified.append(url)

    logger.info(f'There are {len(docs_qualified)} qualified web pages')

    # Stage 5 - Embedd and index documents
    logger.info('Stage 5 - Embedd and index documents')

    if len(urls)>0:
        embed_and_store_documents(vector_store_name, embedding, docs_qualified)

    # Stage 6 - Update ingestion control database
    logger.info('Stage 6 - Update ingestion control database')

    web_data_to_update = parse_ingested_web_data(urls_qualified, urls_disqualified)
    num_updated_ids = update_documents(web_data_to_update)

    logger.info(f'There were {sum(num_updated_ids)} web pages updated')
    
    logger.info('Indexing Pipeline - Finished')


if __name__ == "__main__":

    # Run pipeline

    extract_parse_and_index_web_pages()
