import os

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from agentic_rag_chatbot.utils.config import set_secrets


set_secrets()


groq_api_key = os.environ.get('GROQ_API_KEY', None)
openai_api_key = os.environ.get('OPENAI_API_KEY', None)


def load_groq_llm(model_name: str = 'llama3-70b-8192', model_kwargs: dict[any] = {}, generate_kwargs: dict[any] = {}):

    if groq_api_key is None:
        raise ValueError("GROQ_API_KEY is not set.")

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model_name, 
        model_kwargs=model_kwargs,
        **generate_kwargs
    )

    return llm


def load_openai_llm(model_name: str = 'gpt-4o', model_kwargs: dict[any] = {}, generate_kwargs: dict[any] = {}):
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY is not set.")

    llm = ChatOpenAI(
        api_key=openai_api_key,
        model=model_name, 
        model_kwargs=model_kwargs,
        **generate_kwargs
    )

    return llm


def load_llm(model_provider: str, model_name: str, model_kwargs: dict[any] = {}, generate_kwargs: dict[any] = {}):

    if model_provider=="groq":
        return load_groq_llm(model_name, model_kwargs, generate_kwargs)
    elif model_provider=="openai":
        return load_openai_llm(model_name, model_kwargs, generate_kwargs)
    else:
        raise(f"The code for the model provider {model_provider} must be added!")
