import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
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

# Define a custom function to reverse a string
def reverse_string(s: str) -> str:
    """Reverses the input string."""
    return s[::-1]

# Register the custom function as a tool
reverse_tool = FunctionTool(func=reverse_string, name="reverse_string", description="Reverses the input string.")

# Create an agent with the custom tool
agent = AssistantAgent(
    name="ReverseAgent",
    model_client=openai_client,
    system_message="You are a helpful assistant that can reverse a string using the reverse_string tool",
    tools=[reverse_tool]
)

# Define a task
task = "Reverse the string 'Hello! How are you?'"

# Run the agent
async def main():
    response = await agent.run(task=task)
    print(f"Agent Response: {response.messages[-1].content}")

if __name__ == "__main__":
    asyncio.run(main())
