import asyncio
import streamlit as st
from teams.DSA_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.title("AlgoGenie - Our DSA Problem Solver")
st.write("Welcome to AlgoGenie, your personal DSA Problem Solver! Here you may ask solutions to various data structures and algorithms problems.")

task = st.text_input("Enter your DSA problem here:", value="Write a function to add two numbers.")

async def run(team, docker, task):
    await start_docker_container(docker)

    try:
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print(msg:= f"{message.source}: {message.content}")
                yield msg
            elif isinstance(message, TaskResult):
                print(msg:= f"Stop Reason: {message.stop_reason}")
                yield msg

        print("Task Completed")

    except Exception as e:
        print("Error is: ", e)
    finally:
        await stop_docker_container(docker)

if st.button("Run"):
    st.write("Running the task...")

    team, docker = get_dsa_team_and_docker()

    async def collect_messages():
        async for msg in run(team, docker, task):
            if isinstance(msg, str):
                if msg.startswith("User"):
                    with st.chat_message('user', avatar='👤'):
                        st.markdown(msg)
                elif msg.startswith("DSA_Problem_Solver_Agent"):
                    with st.chat_message('assistant', avatar='🤖'):
                        st.markdown(msg)
                elif msg.startswith("DSA_Code_Executor_Agent"):
                    with st.chat_message('assistant', avatar='💻'):
                        st.markdown(msg)
            elif isinstance(msg, TaskResult):
                st.markdown(f"Stop Reason: {msg.stop_reason}")

    asyncio.run(collect_messages())