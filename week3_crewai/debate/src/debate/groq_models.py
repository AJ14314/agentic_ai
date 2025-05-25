import os
from openai import OpenAI

# Initialize the Groq client
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_URL")
)

def get_llama4_maverick_model():
    return {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "client": groq_client
    }

def get_llama3_70b_model():
    return {
        "model": "llama-3.3-70b-versatile",
        "client": groq_client
    }
