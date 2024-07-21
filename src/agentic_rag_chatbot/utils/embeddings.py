import os
os.environ['HF_HOME'] = ".cache/huggingface"

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from agentic_rag_chatbot.utils.config import set_secrets


set_secrets()


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)


def load_huggingface_embedding_model(model_name: str = "sentence-transformers/all-mpnet-base-v2", model_kwargs: dict={}, encode_kwargs: dict={}, show_progress: bool=False):
    """Load a pretrained text embedding model from HuggingFace"""

    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        show_progress=show_progress
    )

    return embedding_model


def load_openai_embedding_model(model_name: str = "text-embedding-3-large", model_kwargs: dict={}, encode_kwargs: dict={}, show_progress: bool=False):
    """Load a pretrained text embedding model from OpenAI (API)"""

    embedding_model = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        model = model_name,
        model_kwargs=model_kwargs,
        **encode_kwargs,
        show_progress_bar = show_progress
    )

    return embedding_model

    
def load_embedding_model(
        model_provider: str, 
        model_name: str, 
        model_kwargs: dict[any] = {}, 
        encode_kwargs: dict[any] = {},
        show_progress: bool = False
    ):
    """Load a pretrained text embedding model"""

    model_kwargs = model_kwargs if isinstance(model_kwargs, dict) else {}
    encode_kwargs = encode_kwargs if isinstance(encode_kwargs, dict) else {}

    if model_provider=="huggingface":
        return load_huggingface_embedding_model(model_name, model_kwargs, encode_kwargs, show_progress)
    
    elif model_provider=="openai":
        return load_openai_embedding_model(model_name, model_kwargs, encode_kwargs, show_progress)
    else:
        raise(f"The code for the model provider {model_provider} must be added!")
