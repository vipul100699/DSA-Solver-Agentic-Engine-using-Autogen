import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core.tools import FunctionTool
from autogen_agentchat.ui import Console
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not working")

# Initialize the OpenAI model client
openai_client = OpenAIChatCompletionClient(
    model="llama-3.1-8b-instant",
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
    model_info={
        "family": "llama",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
    },
)

assistant_agent = AssistantAgent(
    name="AssistantAgent",
    description="A helpful assistant that can write poetry",
    model_client=openai_client,
    system_message="You are a helpful assistant.",
)

user_proxy_agent = UserProxyAgent(
    name="UserProxyAgent",
    description="A proxy agent that represents the user.",
    input_func=input
)

termination = TextMentionTermination("APPROVE")

# Create a team with the UserProxyAgent and the AssistantAgent
team = RoundRobinGroupChat(
    participants=[assistant_agent, user_proxy_agent],
    termination_condition=termination
)

stream = team.run_stream(task="Write a 4 line poem about the ocean")

async def main():
    await Console(stream)

if __name__ == "__main__":
    asyncio.run(main())
