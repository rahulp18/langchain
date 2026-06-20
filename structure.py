import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel,Field

load_dotenv()

model=init_chat_model(
    model="groq:qwen/qwen3-32b"
)
class Actor(BaseModel):
    name:str=Field(description="Actor Name")
    role:str=Field(description="Actor Role in movie")

class Movie(BaseModel):
    title:str=Field(
        description="This the title of movie",
        min_length=1
    )
    year:int=Field(description="This is the Release YEAR")
    director:str=Field(description="Movie director")
    rating:float=Field(description="The movie rating out of 10")
    actors:list[Actor]=Field(description="Movie Actor names")
    budget:float=Field(description="In India Ruppes")

model_with_structure_outout=model.with_structured_output(Movie)

response=model_with_structure_outout.invoke("Provide details about the movie Sholay")

print(response)

