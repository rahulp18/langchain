import os
from dotenv import load_dotenv
# from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
load_dotenv()

# def get_weather(city:str)->str:
#     """Get the current weather for a city."""
#     return  (
#         f"The weather of {city} is hot. "
#         f"Current temperature is 50°C. "
#         f"Heavy rain is expected tonight."
#     )

# def check_weather():
#     agent=create_agent(
#         model="gpt-5",
#         tools=[get_weather],
#         system_prompt="You are an helpful assistant"
#     )

#     response=agent.invoke({"messages": [
#         {
#             "role":"user",
#             "content":"What is the weather in cuttack?"
#         }
#     ]})
#     print(response)

model=init_chat_model("google_genai:gemini-2.5-flash-lite")

chunks=model.stream("What is thr Future of Software Industry ? and what the Best JOB will OUT i am a Full Stack developer but now i am moving to Python + AI Engineering so what's your thoughts ?")

for chunk in chunks:
    print(chunk.text,end="|" ,flush=True)


