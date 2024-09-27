"""
Information Retrieval Pipeline

This pipeline fetches the most similar docs to a query based on semantic vector search.
"""


from agentic_rag_chatbot.pipelines.information_retrieval.nodes import retrieve_top_k_docs, parse_and_stack_docs_as_string
from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.utils.logging import logger


params = get_params()
params_information_retrieval = params['information_retrieval']
k = params_information_retrieval['number_of_retrieved_docs']
metadata_returned = params_information_retrieval['metadata_returned']


def retrieve_parse_and_stack_top_similar_docs_as_string(query: str):
    """Function to retrieve the most similar docs to a query, parse and stack them as a string"""

    logger.info(f'Retrieves top pages about: {query}')

    # Stage 1 - Retrieve the top similar docs

    retrieved_docs = retrieve_top_k_docs(query, k=k)

    # Stage 2 - Parse and stack retrieved docs as string

    string_docs = parse_and_stack_docs_as_string(retrieved_docs, metadata_returned)
        
    return string_docs


if __name__ == "__main__":

    # EXAMPLE

    query = "What is the goal of Ben Uri Gallery and Museum"

    string_docs = retrieve_parse_and_stack_top_similar_docs_as_string(query)

    print(string_docs)
