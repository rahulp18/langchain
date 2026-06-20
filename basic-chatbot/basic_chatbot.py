# BASIC CHAT BOT with langgraph

from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command,interrupt
from langchain_tavily import TavilySearch

load_dotenv()


memory=MemorySaver()

# TOOLS
@tool
def calculator(num1:int,num2:int,operation)->int:
     """" Perform Mathematical operations
     Operation can be:
     add,subtract,multiply,divide,mod
     """
     print(f"\nTOOL CALLED => {num1} {operation} {num2}\n")
     match operation:
          case "add":
               return num1+num2
          case "multiply":
               return num1*num2
          case "subtract":
               return num1-num2
          case "divide":
               return num1/num2
          case "mod":
               return num1%num2
          case _:
               raise ValueError("Unsupported operation")
     
@tool
def human_assistance(query:str)->str:
     """Request assistance from a human"""
     human_response=interrupt({"query":query})
     return human_response["data"]

class State(TypedDict):
    messages:Annotated[list,add_messages]

search_tool=TavilySearch(
     max_results=5
)

llm=init_chat_model(
    model="groq:qwen/qwen3-32b"
)
llm_with_tools=llm.bind_tools(
     [search_tool]
)

def chatbot(state:State):
    
     response=llm_with_tools.invoke(state["messages"])
     return {
          "messages":[response]
     }
     

graph_builder=StateGraph(State)

graph_builder.add_node(
     "chatbot",
     chatbot
)
graph_builder.add_node("tools",ToolNode([
    #  calculator,
    search_tool 
]))

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges(
     "chatbot",
     tools_condition
)
graph_builder.add_edge(
     "tools",
     "chatbot"
)
 

graph=graph_builder.compile(
     checkpointer=memory
)

print("chatbot started")
print("Type 'exist' to quit\n")
config={
     "configurable":{
          "thread_id":"chat-1"
     },
}

while True:
     user_input=input("You: ")

     if user_input.lower()=="exit":
          break
     result=graph.invoke(
          {
               "messages":[
                    HumanMessage(content=user_input)
               ]
          },
          config=config
     )
     ai_response=result["messages"][-1]
     print(f"\n AI:",ai_response.content)
    #  for chunk,metadata in graph.stream(
    #      {
    #           "messages":[
    #                HumanMessage(content=user_input)
    #           ],
              
    #      },
    #      config=config,
    #      stream_mode="messages"
    # ):
    #   print(chunk.content,end="",flush=True)
     

