from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.pipelines.agent.nodes import llm, tools, prompt
from langchain.agents import AgentExecutor, create_openai_tools_agent


params = get_params()
params_agent = params['agent']
verbose = params_agent['verbose']


# Instantiate a agent and agent executor

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=verbose)


def generate_user_response(input: str, chat_history: list[str] = []):

    agent_response = agent_executor.invoke(
        {
            "chat_history": chat_history,
            "input": input
        }
    )

    return agent_response['output']


if __name__ == "__main__":
    #Example
    
    from langchain.schema import AIMessage, HumanMessage

    input = "Hi there, how can you assist me?"

    print(f"Human: {input}")

    output = generate_user_response(input)

    print(f"AI: {output}")

    chat_history = [
        HumanMessage(content=input),
        AIMessage(content=output)
    ]

    input = "What are contributions of Refugee to British visual culture?"

    print(f"Human: {input}")

    output = generate_user_response(input, chat_history)

    print(f"AI: {output}")
