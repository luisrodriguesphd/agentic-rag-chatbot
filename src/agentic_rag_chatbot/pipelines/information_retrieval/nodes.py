from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.utils.embeddings import load_embedding_model
from langchain.docstore.document import Document
from agentic_rag_chatbot.utils.vector_store import load_vector_store


params = get_params()
vector_store_name = params['data_indexing']['vector_store_name']
embedding_model = params['embedding_model']


# Load embeddings into Chroma from disk
# See: https://python.langchain.com/docs/integrations/vectorstores/chroma
embedding = load_embedding_model(embedding_model['model_provider'], embedding_model['model_name'], embedding_model['model_kwargs'], embedding_model['encode_kwargs'])
vectordb = load_vector_store(vector_store_name, embedding)


def retrieve_top_k_docs(query: str, k: int=3):
    """Function to retrieve the most similar docs to a query"""

    # For complex queries, use MongoDB-like operators:
    #   $gt, $gte, $lt, $lte, $ne, $eq, $in, $nin
    # Example from resume-worth:
    #   'filter': {"job_title": {"$in": job_titles}}
    # See: https://www.mongodb.com/docs/manual/reference/operator/query/
    retriever = vectordb.as_retriever(
        search_type='similarity',
        search_kwargs={
            'k': k,
        },
    )

    # Retrieve top vacancies with the job title
    retrieved_docs = retriever.invoke(query)

    return retrieved_docs


def parse_and_stack_docs_as_string(docs: Document, metadata_returned: list[str] = ['source']):
    """Function to parse docs and stack them as string"""

    string_docs = ""
    for doc in docs:
        string_doc = ""
        for metadata_name in metadata_returned:
            try:
                metadata_content = doc.metadata[metadata_name] 
                string_doc = "\n".join([string_doc, f"{metadata_name}: {metadata_content}"])
            except:
                pass
        string_doc = "\n".join([string_doc, f"content: {doc.page_content}"])
        string_docs = "\n\n".join([string_docs, string_doc])

    return string_docs
