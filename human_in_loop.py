from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from langgraph.types import Command
load_dotenv()

# Tools declaration

def read_email_tool(email_id:str)->str:
    """"Mock Function to read an email by it's ID. """
    return f"Email content for ID {email_id}"
def send_email_tool(recipient:str,subject:str,body:str)->str:
    """"Mock function to send an Email"""
    return f"Email sent to {recipient} with subject {subject} and content {body}"

agent=create_agent(
    model="gpt-4o-mini",
    tools=[
        read_email_tool,
        send_email_tool
    ],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email_tool":{
                    "allowed_decisions":["approve","edit","reject"]
                },
                "read_email_tool":False
            }
        )
    ]
)

config={"configurable":{"thread_id":"test-approve"}}

result=agent.invoke(
    {"messages":[HumanMessage(content="Send email  to rahul@gmail.com With Subject Offer Letter and body Congratulation you are selected in Google")]},
    config=config
)
if "__interrupt__" in result:
    print("\n=== HUMAN APPROVAL REQUIRED ===\n")
    result=agent.invoke(
        Command(
            resume={
                "decisions":[
                    {
                        "type":"edit",
                        "edited_action":{
                            "name":"send_email_tool",
                            "args":{
                                "recipient":"guni@gmail.com",
                                "subject":"Best Of Luck",
                                "body":"This was edited by Human before sending"
                            }
                        }
                    }
                ]
            }
        ),
        config=config
    )
print("\n=== FINAL RESPONSE ===\n")
print(f"Result {result['messages'][-1].content}")
 
 