"""
Data Collection Pipeline

Data collection is the process of extracting and gathering relevant information from various web sources to build a comprehensive dataset.

This pipeline involves crawling the web pages, extracting the textual content, cleaning and structuring the data, and storing the processed text in a structured database.
"""

from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.pipelines.data_collection.nodes import crawl_site_to_fetch_urls, parse_collected_web_data
from agentic_rag_chatbot.utils.database import insert_documents, get_previously_collected_urls, update_documents
from agentic_rag_chatbot.utils.logging import logger


params = get_params()
start_page = params['data_collection']['start_page']
min_length_text_body = params['data_collection']['min_length_text_body']
max_number_visited_urls = params['data_collection']['max_number_visited_urls']
max_number_qualified_urls = params['data_collection']['max_number_qualified_urls']


def collect_parse_and_store_web_pages():

    logger.info('Collection pipeline - Started')

    # Stage 1 - Get web pages previously collected
    logger.info('Stage 1 - Get web pages previously collected')

    visited_urls_previously, urls_to_visit_previously = get_previously_collected_urls()

    # Stage 2 - Crawl web pages to ingest 
    logger.info(f'Stage 2 - Crawl (up to {min(max_number_visited_urls, max_number_qualified_urls)}) web pages to ingest')

    qualified_urls, visited_urls, urls_to_visit = crawl_site_to_fetch_urls(
        start_url=start_page, 
        min_length_text_body = min_length_text_body,
        max_number_visited_urls = max_number_visited_urls,
        max_number_qualified_urls = max_number_qualified_urls,
        visited_urls = visited_urls_previously,
        urls_to_visit = urls_to_visit_previously,
    )

    # Stage 3 - Parse the collected web pages
    logger.info('Stage 3 - Parse the collected web pages')

    web_data_to_update, web_data_to_add = parse_collected_web_data(qualified_urls, visited_urls, urls_to_visit, visited_urls_previously, urls_to_visit_previously)
    
    # Stage 4 - Insert and update into the database
    logger.info('Stage 4 - Insert and update into the database')

    # Update the data into the collection
    if web_data_to_update:
        num_updated_ids = update_documents(web_data_to_update)

        logger.info(f'There were {sum(num_updated_ids)} web pages updated')

    # Inserting the data into the collection
    if web_data_to_add:
        inserted_ids = insert_documents(web_data_to_add)

        logger.info(f'There were {len(inserted_ids)} web pages inserted')

    logger.info('Collection Pipeline - Finished')


if __name__ == "__main__":

    # Run pipeline

    collect_parse_and_store_web_pages()
