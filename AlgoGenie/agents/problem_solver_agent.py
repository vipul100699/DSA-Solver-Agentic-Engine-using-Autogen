from autogen_agentchat.agents import AssistantAgent
from AlgoGenie.config.settings import get_model_client

model_client = get_model_client()

def get_problem_solver_agent():
    """
    Function to get the problem solver agent.
    This agent is responsible for solving the DSA problems.
    It will work with the code executor agent to execute the code.
    """
    
    problem_solver_agent = AssistantAgent(
        name="DSA_Problem_Solver_Agent",
        description="An Agent that solves DSA Problems",
        model_client=model_client,
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

    return problem_solver_agent