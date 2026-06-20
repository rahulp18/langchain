from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage,SystemMessage


load_dotenv()

# Summarization middleware of langchain
agent=create_agent(
    model="gpt-4o-mini",
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("messages",10),
            keep=("messages",4)
        )
    ]
)

config={"configurable":{"thread_id":"test-1"}}

questions=[
    "What is the future of Software Engineering?",
    "If my Friend completed her 12th Exam with 86% CHSE board will you recommend her to come to this IT Industry. her Goal is to become an Financial Independent women",
    "I am a Software Developer(Full Stack) Learning Python +FastAPI + RAG+ Langchain is it worth it or not ?",
    "What to Create  a Successful business?",
    "How to Set Weekend's for an Better Learning Days",
    "Now my salary is 65k inhand per month how to ask for more i am 3+ yrs experience software developer with Skills, React,Next,Nest,Graphql,Prisma,Keystone,Express,Python,FastAPI,Postgress,Claude AI,RAG"
]

for q in questions:
    response=agent.invoke({"messages":[HumanMessage(content=q)]},config=config)
    print(f"Response {response}\n")
    print(len(response["messages"]))