import os
from dotenv import load_dotenv
from config.constant import MODEL, BASE_URL
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not working")


def get_model_client():
    """Returns the model client"""

    model_client = OpenAIChatCompletionClient(
        model=MODEL,
        api_key=api_key,
        base_url=BASE_URL,
        model_info={
            "family": "llama",
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
        },
    )

    return model_client