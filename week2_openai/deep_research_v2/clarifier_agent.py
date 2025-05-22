# clarifier_agent.py

from typing import List
from pydantic import BaseModel
from agents import Agent
from groq_client import get_groq_model

class ClarificationData(BaseModel):
    questions: List[str]

CLARIFY_INSTRUCTIONS = """
You are a Research Clarifier. Given a user’s research query, generate exactly 3 clarifying questions
that will help focus and refine that query. Return only JSON matching the ClarificationData model.
"""

clarifier_agent = Agent(
    name="ClarifierAgent",
    instructions=CLARIFY_INSTRUCTIONS,
    model=get_groq_model(),
    output_type=ClarificationData,
)
