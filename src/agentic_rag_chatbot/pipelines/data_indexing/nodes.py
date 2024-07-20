import re

from agentic_rag_chatbot.utils.embeddings import load_embedding_model
from langchain_community.document_loaders import WebBaseLoader
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma


def extract_and_parse_webpages(webpage_urls: str) -> list[Document]:
    """Extract webpages and parse as LangChain's Documents"""

    loader = WebBaseLoader(webpage_urls)
    loader.requests_per_second = 1
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


def index_documents(docs: list[Document], persist_directory: str, embedding_model: dict):
    """Function to embed and index the documents in Chroma vector database"""

    # Load a pretrained text embedding model

    embedding_function = load_embedding_model(embedding_model['model_provider'], embedding_model['model_name'], embedding_model['model_kwargs'], embedding_model['encode_kwargs'], embedding_model['show_progress'])

    # Create text embeddings and store in a vector database Chroma. For more options, see: 
    #   https://python.langchain.com/docs/modules/data_connection/vectorstores/
    #   https://python.langchain.com/docs/integrations/vectorstores/chroma

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding_function,
        persist_directory=persist_directory
    )

    return vectordb
