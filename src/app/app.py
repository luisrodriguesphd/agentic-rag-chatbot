import gradio as gr

from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.pipelines.agent.pipeline import generate_user_response
from langchain.schema import AIMessage, HumanMessage


params = get_params()
app_config = params['app_config']
app_backend = params['app_backend']
app_frontend = params['app_frontend']


def invoke(input, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    output = generate_user_response(input, history_langchain_format)
    return output


def vote(data: gr.LikeData):
    if data.liked:
        print("[+1] User upvoted this response:\n" + data.value)
    else:
        print("[-1] User downvoted this response:\n" + data.value)


# Gradio References:
#   https://www.gradio.app/docs/gradio/chatinterface
#   https://www.gradio.app/guides/creating-a-chatbot-fast
with gr.Blocks(title=app_frontend['title']) as demo:
    chatbot = gr.Chatbot(placeholder=app_frontend['description'])
    chatbot.like(vote, None, None)
    gr.ChatInterface(
        fn=invoke, 
        chatbot=chatbot,
        examples= app_frontend['examples']
    )


if __name__ == "__main__":
    # To see changes in real-time, instead of the python command, use: gradio src\app\app.py
    # Use share=True to create a public link to share. This share link expires in 72 hours.
    demo.launch(share=False, server_name=app_config['host'], server_port=app_config['port'])
