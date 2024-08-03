import os

from agentic_rag_chatbot.utils.config import get_params, set_secrets
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from typing import Any, Dict, List, Optional, Tuple


set_secrets()
MONGODB_ATLAS_CLUSTER_URI = os.environ.get('MONGODB_ATLAS_CLUSTER_URI')
MONGODB_ATLAS_DB_NAME = os.environ.get('MONGODB_ATLAS_DB_NAME')
MONGODB_ATLAS_VECTOR_COLLECTION_NAME = os.environ.get('MONGODB_ATLAS_VECTOR_COLLECTION_NAME')
MONGODB_ATLAS_VECTOR_INDEX_NAME = os.environ.get('MONGODB_ATLAS_VECTOR_INDEX_NAME')


params = get_params()
embedding_dir = params['embedding_dir']


try:
    # Connect to the MongoDB client
    client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

    # Select the collection from a database
    collection = client[MONGODB_ATLAS_DB_NAME][MONGODB_ATLAS_VECTOR_COLLECTION_NAME]
except:
    pass


def load_vector_store(vector_store_name: str, embedding_model):
    """Load a vector store"""

    if vector_store_name=="chroma":
        return Chroma(
            embedding_function=embedding_model,
            persist_directory=embedding_dir, 
        )
    elif vector_store_name=="mongodb":
        return MongoDBAtlasVectorSearch(
            embedding=embedding_model,
            collection=collection,
            index_name=MONGODB_ATLAS_VECTOR_INDEX_NAME,
        )
    else:
        raise(f"The code for the vector store {vector_store_name} must be added!")


def embed_and_store_documents(vector_store_name: str, embedding, docs: list[Document]):
    """Embed and index the documents in Chroma vector store"""

    if vector_store_name=="chroma":
        Chroma.from_documents(
            documents=docs,
            embedding=embedding,
            persist_directory=embedding_dir
        )
    elif vector_store_name=="mongodb":
        MongoDBAtlasVectorSearch.from_documents(
            documents=docs,
            embedding=embedding,
            collection=collection,
            index_name=MONGODB_ATLAS_VECTOR_INDEX_NAME,
        )
    else:
        raise(f"The code for the vector store {vector_store_name} must be added!")
