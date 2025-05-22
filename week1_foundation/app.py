from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
import json
import os
import requests
from PyPDF2 import PdfReader
import gradio as gr
from pydantic import BaseModel


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

class Me:

    def __init__(self):
        self.gemini = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.GEMINI_MODEL = "gemini-2.5-flash-preview-04-17"
        self.OPENROUTER_MODEL = "meta-llama/llama-3.3-8b-instruct:free"
        self.evaluation_model = ""
        self.openrouter = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        self.name = "Anand Jain"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text

        reader = PdfReader("me/resume.pdf")
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results

    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s AI assistant include name of the person always for every greetings, \
Always start with a warm welcome message to new visitors, introducing yourself as {self.name}'s AI assistant. \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If some asks for looking for job change ask for their email and record it using your record_user_details tool then provide them the my email address \
Be especially helpful to recruiters or potential employers by highlighting {self.name}'s key achievements and skills relevant to their questions. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def evaluator_system_prompt(self):
        evaluator_system_prompt = (
            f"You are an evaluator that decides whether a response to a question is acceptable. "
            f"You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. "
            f"The Agent is playing the role of {self.name} and is representing {self.name} on their website. "
            f"The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. "
            f"The Agent has been provided with context on {self.name} in the form of their summary, LinkedIn details and resume. Here's the information:"
        )

        evaluator_system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Resume Content:\n{self.resume}\n\n"
        evaluator_system_prompt += f"With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."
        return evaluator_system_prompt

    def evaluator_user_prompt(self,reply, message, history):
        user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
        user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
        user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
        user_prompt += f"Please evaluate the response, replying with whether it is acceptable and your feedback."
        return user_prompt

    def evaluate(self,reply, message, history) -> Evaluation:

        try:
            # First attempt with OpenRouter
            messages = [{
                "role": "system",
                "content": self.evaluator_system_prompt()
            }] + [{
                "role": "user",
                "content": self.evaluator_user_prompt(reply, message, history)
            }]

            print(f"Attempting evaluation with OpenRouter model: {self.OPENROUTER_MODEL}")
            # Artificially inject RateLimitError for testing
            # DEBUG_FORCE_RATE_LIMIT = os.getenv("DEBUG_FORCE_RATE_LIMIT", "false").lower() == "true"
            # if DEBUG_FORCE_RATE_LIMIT:
            #     raise RateLimitError(
            #         message="Rate limit exceeded (test)",
            #         body={
            #             "error": {
            #                 "message": "Rate limit exceeded: free-models-per-day",
            #                 "code": 429,
            #                 "metadata": {
            #                     "headers": {
            #                         "X-RateLimit-Limit": "50",
            #                         "X-RateLimit-Remaining": "0",
            #                         "X-RateLimit-Reset": "1747872000000"
            #                     }
            #                 }
            #             },
            #             "user_id": "test_user"
            #         },
            #         code=429
            #     )

            response = self.openrouter.beta.chat.completions.parse(
                model=self.OPENROUTER_MODEL,
                messages=messages,
                response_format=Evaluation
            )

            self.evaluation_model = self.OPENROUTER_MODEL
            return response.choices[0].message.parsed

        except Exception as e:
            print("OpenRouter rate limit exceeded - falling back to Gemini", e)

            # Direct fallback to Gemini
            messages = [{
                "role": "system",
                "content": self.evaluator_system_prompt()
            }] + [{
                "role": "user",
                "content": self.evaluator_user_prompt(reply, message, history)
            }]

            print(f"Using Gemini model: {self.GEMINI_MODEL}")
            response = self.gemini.beta.chat.completions.parse(
                model=self.GEMINI_MODEL,
                messages=messages,
                response_format=Evaluation
            )

            self.evaluation_model = self.GEMINI_MODEL
            return response.choices[0].message.parsed

    def rerun(self, reply, message, history, feedback):
        updated_system_prompt = self.system_prompt() + f"\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
        updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
        updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
        messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
        response = self.gemini.chat.completions.create(model=self.GEMINI_MODEL, messages=messages)
        return response.choices[0].message.content

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        response = None  # Initialize response outside loop

        while not done:
            response = self.gemini.chat.completions.create(
                model=self.GEMINI_MODEL,
                messages=messages,
                tools=tools
            )

            if response.choices[0].finish_reason == "tool_calls":
                message_obj = response.choices[0].message
                tool_calls = message_obj.tool_calls

                results = self.handle_tool_call(tool_calls)

                # Append assistant's tool call and tool responses
                messages.append(message_obj)
                messages.extend(results)

            else:
                done = True

        # Evaluate the final response
        evaluation = self.evaluate(response.choices[0].message.content, message, history)

        if evaluation.is_acceptable:
            print(f"Passed evaluation from {self.evaluation_model} - returning reply")
            return response.choices[0].message.content
        else:
            print("Failed evaluation - retrying")
            print(evaluation.feedback)
            self.rerun(response.choices[0].message.content, message, history, evaluation.feedback)
            return response.choices[0].message.content  # Or handle rerun differently


if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
