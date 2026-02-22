from autogen_agentchat.agents import CodeExecutorAgent
from config.docker_executor import get_docker_executor

def get_code_executor_agent():
    """
    Function to get the code executor agent.
    This agent is responsible for executing the code.
    It will execute the code written by the problem solver agent.
    """
    docker = get_docker_executor()
    code_executor_agent = CodeExecutorAgent(
        name="DSA_Code_Executor_Agent",
        code_executor=docker
    )

    return code_executor_agent, docker