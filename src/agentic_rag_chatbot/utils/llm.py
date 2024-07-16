import os

from langchain.callbacks.base import BaseCallbackHandler
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from agentic_rag_chatbot.utils.config import set_secrets


set_secrets()


groq_api_key = os.environ.get('GROQ_API_KEY', None)
openai_api_key = os.environ.get('OPENAI_API_KEY', None)


class PromptPrintingCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        pass

    def on_llm_start(self, serialized, prompts, **kwargs):
        for prompt in prompts:
            print(f"\n\n<-----\nSTART Prompt:\n{prompt}\nPrompt END----->\n\n")

    def on_llm_end(self, result, **kwargs):
        pass


def load_groq_llm(
        model_name: str = 'llama3-70b-8192', 
        model_kwargs: dict[any] = {}, 
        generate_kwargs: dict[any] = {}, 
        debug_mode: bool = False
    ):

    if groq_api_key is None:
        raise ValueError("GROQ_API_KEY is not set.")

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model_name, 
        model_kwargs=model_kwargs,
        **generate_kwargs
    )
    
    if debug_mode: 
        callback = PromptPrintingCallbackHandler()
        llm.callbacks=[callback]

    return llm


def load_openai_llm(
        model_name: str = 'gpt-4o', 
        model_kwargs: dict[any] = {}, 
        generate_kwargs: dict[any] = {}, 
        debug_mode: bool = False
    ):
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY is not set.")

    llm = ChatOpenAI(
        api_key=openai_api_key,
        model=model_name, 
        model_kwargs=model_kwargs,
        **generate_kwargs
    )

    if debug_mode: 
        callback = PromptPrintingCallbackHandler()
        llm.callbacks=[callback]

    return llm


def load_llm(
        model_provider: str, 
        model_name: str, 
        model_kwargs: dict[any] = {}, 
        generate_kwargs: dict[any] = {},
        debug_mode: bool = False
    ):

    if model_provider=="groq":
        return load_groq_llm(model_name, model_kwargs, generate_kwargs, debug_mode)
    elif model_provider=="openai":
        return load_openai_llm(model_name, model_kwargs, generate_kwargs, debug_mode)
    else:
        raise(f"The code for the model provider {model_provider} must be added!")
