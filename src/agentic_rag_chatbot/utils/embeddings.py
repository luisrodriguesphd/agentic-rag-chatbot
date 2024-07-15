import os
os.environ['HF_HOME'] = ".cache/huggingface"

from langchain_huggingface.embeddings import HuggingFaceEmbeddings


def load_embedding_model(model_name: str = "sentence-transformers/all-mpnet-base-v2", model_kwargs: dict={}, encode_kwargs: dict={}, show_progress: bool=False):
    """Load a pretrained text embedding model"""

    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        show_progress=show_progress,
    )

    return embedding_model
