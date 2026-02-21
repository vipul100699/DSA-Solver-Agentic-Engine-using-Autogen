from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
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

async def main():

    docker = DockerCommandLineCodeExecutor(
        work_dir="temp",
        timeout=120
    )

    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutorAgent",
        code_executor=docker
    )

#     task = TextMessage(
#         content='''
# ```python
# print('Hello World')
# ```
#     ''',
#         source="user",
#     )

    problem_solver_agent = AssistantAgent(
        name="DSA_Problem_Solver_Agent",
        description="An Agent that solves DSA Problems",
        model_client=openai_client,
        system_message='''
            You are a problem solver agent that is an expert in solving DSA problems.
            You will be working with code executor agent to execute the code.
            You will be given a task and you should:
            1. Understand the problem
            2. Think step by step
            3. At the beginning of the response, you have to specify your plan to solve the task.
            4. Then you should give the code in a code block (Python).
            5 You should write code in one code block at a time and then pass it to the code executor agent to execute it.
            6. Make sure to have at least 3 test cases for the code you write. 
            7. Once the code has been executed and if the same has been done successfully, you have the results.
            8. You should explain the code execution results.

            At the end, once the code has been executed successfully, you have to say "STOP" to stop the conversation.
            '''        
    )

    termination_condition = TextMentionTermination("STOP")

    team = RoundRobinGroupChat(
        participants=[problem_solver_agent, code_executor_agent],
        termination_condition=termination_condition,
        max_turns=10
    )

    try:
        await docker.start()
        task = "Write a python code to add two numbers."

        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print("=="*20)
                print(message.source, ":", message.content)
                print("=="*20)
            elif isinstance(message, TaskResult):
                print("Stop Reason: ", message.stop_reason)

        # result = await code_executor_agent.on_messages(
        #     [task],
        #     cancellation_token=CancellationToken()
        # )
        # print("Result is: ", result.chat_message.content)

    except Exception as e:
        print("Error is: ", e)
    finally:
        await docker.stop()


if __name__ == "__main__":
    asyncio.run(main())
