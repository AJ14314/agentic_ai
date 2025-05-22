from agents import OpenAIChatCompletionsModel, AsyncOpenAI
import os

def get_groq_model():
    """Returns a configured OpenAIChatCompletionsModel for Groq."""
    groq_url = os.getenv("GROQ_URL")
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_model_name = os.getenv("GROQ_MODEL_LLAMA4_SCOUT")

    if not all([groq_url, groq_api_key, groq_model_name]):
        raise ValueError("Missing one or more required GROQ environment variables.")

    groq_client = AsyncOpenAI(base_url=groq_url, api_key=groq_api_key)

    return OpenAIChatCompletionsModel(
        model=groq_model_name,
        openai_client=groq_client
    )
