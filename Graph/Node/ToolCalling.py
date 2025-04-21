from Config.llm import llm
from Graph.Tool.Tools import get_vector_response
from Graph.OutputParser.parsers import FinalOutput
from Graph.Prompt.prompts import Agent_prompt
from langgraph.prebuilt.chat_agent_executor import create_react_agent




tools_list = [get_vector_response]

AgentToolCall = create_react_agent(
    llm,
    tools=tools_list,
    response_format=FinalOutput, 
    prompt=Agent_prompt,  
    )
