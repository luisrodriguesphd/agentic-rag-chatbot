import os

from agentic_rag_chatbot.utils.config import set_secrets
from pymongo import MongoClient
from pymongo.results import InsertManyResult, UpdateResult
from typing import Any, Dict, List, Tuple


set_secrets()


MONGODB_ATLAS_CLUSTER_URI = os.environ.get('MONGODB_ATLAS_CLUSTER_URI')
MONGODB_ATLAS_DB_NAME = os.environ.get('MONGODB_ATLAS_DB_NAME')
MONGODB_ATLAS_INGESTION_COLLECTION_NAME = os.environ.get('MONGODB_ATLAS_INGESTION_COLLECTION_NAME')

# Connect to the MongoDB client
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

# Select the collection from a database
collection = client[MONGODB_ATLAS_DB_NAME][MONGODB_ATLAS_INGESTION_COLLECTION_NAME]


def insert_documents(docs: List[Dict[str, Any]]) -> List[str]:
    """
    Inserts a list of documents into a MongoDB collection and returns the IDs of the inserted documents.

    Args:
    docs (List[dict]): A list of dictionaries, each representing a document to be inserted.

    Returns:
    List[str]: A list of string representations of the inserted documents' ObjectIds.
    """
    result: InsertManyResult = collection.insert_many(docs)
    inserted_ids: List[str] = [str(object_id) for object_id in result.inserted_ids]
    return inserted_ids


def update_documents(docs: List[dict], filter_field: str = 'url') -> List[int]:
    """
    Updates a list of documents in a MongoDB collection based on a specified filter field
    and returns the count of documents updated for each update operation.

    Args:
    docs (List[dict]): A list of dictionaries, each representing updated data for documents.
    filter_field (str): The field name used to filter documents for updating.

    Returns:
    List[int]: A list of counts of the documents updated in each update operation.
    """
    num_updated_ids: List[int] = []
    for doc in docs:
        filter_dict = {filter_field: doc[filter_field]}
        # Remove the filter field from the document before updating
        new_values = {"$set": {key: doc[key] for key in doc if key != filter_field}}
        
        result: UpdateResult = collection.update_one(filter_dict, new_values)
        num_updated_ids.append(result.modified_count)
    return num_updated_ids


def delete_documents(query: Dict = {}) -> int:
    """
    Deletes documents from a specified MongoDB collection based on a query and returns the count of deleted documents.

    Args:
    query (dict, optional): A dictionary specifying the deletion criteria. Defaults to an empty dictionary, which matches all documents.

    Returns:
    int: The number of documents deleted.
    """
    result = collection.delete_many(query)
    num_deleted_ids = result.deleted_count
    
    return num_deleted_ids


def get_previously_collected_urls() -> Tuple[List[str], List[str]]:
    """
    Retrieves lists of URLs from a MongoDB collection, categorized into previously visited and to-be-visited.

    Returns:
    Tuple[List[str], List[str]]: A tuple containing two lists:
        - The first list contains URLs that have been marked as visited (is_visited=True).
        - The second list contains URLs that are marked to be visited (is_visited=False).
    """
    # Retrieve URLs that have been visited
    visited_urls_previously: List[str] = [data['url'] for data in collection.find({"is_visited": True})]

    # Retrieve URLs that have not been visited yet
    urls_to_visit_previously: List[str] = [doc['url'] for doc in collection.find({"is_visited": False})]

    return visited_urls_previously, urls_to_visit_previously


def get_urls_to_ingest() -> Tuple[List[str], List[str]]:
    """
    Retrieves lists of URLs from a MongoDB collection, categorized as .

    Returns:
    List[str]: A list of URLs that must be ingested (is_to_ingest=True).
    """

    urls_to_ingest: List[str] = [data['url'] for data in collection.find({"is_to_ingest": True})]

    return urls_to_ingest
