import wikipedia

from agentic_rag_chatbot.pipelines.information_retrieval.pipeline import retrieve_parse_and_stack_top_similar_docs_as_string
from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.utils.llm import load_llm
from langchain.agents import tool
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate
)


params = get_params()
params_generative_model = params['generative_model']
debug_mode = params_generative_model['debug_mode']
model_provider = params_generative_model['model_provider']
model_name = params_generative_model['model_name']
model_kwargs = params_generative_model['model_kwargs']
generate_kwargs = params_generative_model['generate_kwargs']
system_message = params_generative_model['system_message']
params_agent = params['agent']
tool_names = params_agent['tool_names']


# Load LLM

llm = load_llm(model_provider, model_name, model_kwargs, generate_kwargs, debug_mode)


# Instantiate a prompt template

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            f"""{system_message}\nConversation context:"""
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# Define tools

@tool
def search_wikipedia(query: str) -> str:
    """
    Searches Wikipedia for a given query and returns summaries of the top results.

    This function performs a search on Wikipedia for the specified query, retrieves the top three search results, 
    and returns a summary of each. If the retrieval fails for a particular page, it is skipped. If no summaries 
    are retrieved, it returns a message indicating no suitable results were found.

    Args:
        query (str): The search query to be used for retrieving information from Wikipedia.

    Returns:
        str: A string that concatenates the page title and summary of each of the top three search results,
             separated by double newlines. If no results are found or summaries are retrieved, a message is returned
             indicating the absence of good results.
    """
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[:3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except:
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)


@tool()
def search_ben_uri_gallery_and_museum(query: str) -> str:
    """
    Useful to retrieve content from Ben Uri Gallery and Museum website for a given query.

    Ben Uri Gallery and Museum's content focusing on the contributions of Jewish, Refugee, and Immigrant artists to 
    British visual culture.

    Args:
        query (str): The search query for which the information is to be retrieved from the Ben Uri gallery and museum.

    Returns:
        str: A string that concatenates the web page link and a significant text chunk for each of the top three results,
             separated by double newlines. If no relevant results are found, a message is returned indicating the absence 
             of useful information.
    """
    
    results_stacked_as_string = retrieve_parse_and_stack_top_similar_docs_as_string(query)

    return results_stacked_as_string


tool_mapping = {
    "search_wikipedia": search_wikipedia,
    "search_ben_uri_gallery_and_museum": search_ben_uri_gallery_and_museum
}


tools = [tool_mapping[tool_name] for tool_name in tool_names]
