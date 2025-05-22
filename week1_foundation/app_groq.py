from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
import json
import os
import time
import requests
from PyPDF2 import PdfReader
import gradio as gr
from pydantic import BaseModel


load_dotenv(override=True)


def push(text):
    requests.post(
        os.getenv("PUSHOVER_URL"),
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        },
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
                "description": "The email address of this user",
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it",
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered",
            },
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]


class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str


class Me:

    def __init__(self):
        self.gemini = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_URL"),
        )
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL")
        self.LLAMA3_3_MODEL = os.getenv("GROQ_MODEL_LLAMA4_MAV")
        self.evaluation_model = ""
        self.llama3_3_groq = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url=os.getenv("GROQ_URL"),
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
            results.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                }
            )
        return results

    def system_prompt(self):
        system_prompt = (
            f"You are acting as {self.name}, an AI assistant representing them on their website. "
            f"Always begin with a warm welcome message and introduce yourself as {self.name}'s AI assistant. "
            f"Include {self.name}'s name in all greetings.\n\n"
            f"You specialize in answering questions about {self.name}'s career, background, skills, and experience. "
            f"Your job is to faithfully represent {self.name} in all conversations, as if you're speaking to a potential client or employer.\n\n"
            f"You are provided with a summary of {self.name}'s background, LinkedIn profile, and resume, which you should use to inform your responses. "
            f"Be professional and engaging at all times.\n\n"
            f"If someone expresses interest in job opportunities or mentions looking for a job change, politely ask for their email "
            f"and record it using the `record_user_details` tool. Then, provide them with {self.name}'s email address.\n\n"
            f"Be especially helpful to recruiters or hiring managers by highlighting {self.name}'s key achievements and relevant skills.\n\n"
            f"If you're ever unsure of an answer, even if it's unrelated to {self.name}'s career, use the `record_unknown_question` tool "
            f"to log the question.\n\n"
            f"If a user is casually engaging, try to guide the conversation toward establishing contact. Ask for their email and log it "
            f"with the `record_user_details` tool."
        )

        # Add personal data summaries
        system_prompt += (
            f"\n\n## Summary:\n{self.summary}\n\n"
            f"## LinkedIn Profile:\n{self.linkedin}\n\n"
            f"## Resume:\n{self.resume}\n\n"
            f"With this context, please chat with the user, always staying in character as {self.name}."
        )

        return system_prompt

    def evaluator_system_prompt(self):
        evaluator_system_prompt = (
            f"You are an evaluator tasked with judging whether an Agent's latest response in a conversation is of acceptable quality.\n\n"
            f"You are given a conversation between a User and an Agent. The Agent is acting as {self.name} and is representing them professionally "
            f"on their personal website.\n\n"
            f"The Agent is expected to be professional, helpful, and engaging—especially when interacting with potential clients or employers. "
            f"The Agent has access to {self.name}'s background through a summary, LinkedIn profile, and resume.\n\n"
            f"Here is the contextual information provided to the Agent:"
        )

        evaluator_system_prompt += (
            f"\n\n## Summary:\n{self.summary}\n\n"
            f"## LinkedIn Profile:\n{self.linkedin}\n\n"
            f"## Resume:\n{self.resume}\n\n"
            f"Based on this context, evaluate the Agent’s most recent response. "
            f"Reply with a clear judgment on whether the response is acceptable and provide your feedback."
        )

        return evaluator_system_prompt

    def evaluator_user_prompt(self, reply, message, history):
        user_prompt = (
            "You are provided with a conversation between a User and an Agent.\n\n"
            f"## Conversation History:\n{history}\n\n"
            f"## Latest User Message:\n{message}\n\n"
            f"## Agent's Response:\n{reply}\n\n"
            "Please evaluate the Agent's latest response. Reply with whether it is acceptable, and include clear, constructive feedback."
        )
        return user_prompt

    def evaluate(self, reply, message, history) -> Evaluation:

        try:
            # First attempt with Groq LLAMA Model
            messages = [
                {"role": "system", "content": self.evaluator_system_prompt()},
                {
                    "role": "user",
                    "content": self.evaluator_user_prompt(reply, message, history),
                },
            ]

            print(f"Attempting evaluation with Groq LLAMA model: {self.LLAMA3_3_MODEL}")
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

            response = self.llama3_3_groq.beta.chat.completions.parse(
                model=self.LLAMA3_3_MODEL,
                messages=messages,
                response_format=Evaluation,
            )

            self.evaluation_model = self.LLAMA3_3_MODEL
            return response.choices[0].message.parsed

        except Exception as e:
            print("Groq rate limit exceeded - falling back to Gemini", e)

            # Direct fallback to Gemini
            messages = [
                {"role": "system", "content": self.evaluator_system_prompt()},
                {
                    "role": "user",
                    "content": self.evaluator_user_prompt(reply, message, history),
                },
            ]

            print(f"Using Gemini model: {self.GEMINI_MODEL}")
            response = self.gemini.beta.chat.completions.parse(
                model=self.GEMINI_MODEL, messages=messages, response_format=Evaluation
            )

            self.evaluation_model = self.GEMINI_MODEL
            return response.choices[0].message.parsed

    def rerun(self, reply, message, history, feedback):
        # Build the updated system prompt with rejection feedback
        updated_system_prompt = (
            self.system_prompt() + "\n\n## Previous Answer Rejected\n"
            "Your previous response was rejected during quality control.\n"
            "Please revise it, considering the feedback below.\n\n"
            f"### Attempted Answer:\n{reply}\n\n"
            f"### Rejection Reason:\n{feedback}\n"
        )

        # Compose full message sequence
        messages = (
            [{"role": "system", "content": updated_system_prompt}]
            + history
            + [{"role": "user", "content": message}]
        )

        # Generate revised response using the model
        response = self.llama3_3_groq.chat.completions.create(
            model=self.LLAMA3_3_MODEL, messages=messages
        )

        return response.choices[0].message.content

    def clean_history(self, messages):
        return [
            {"role": m["role"], "content": m["content"]}
            for m in messages
            if "role" in m and "content" in m
        ]

    def chat(self, message, history):
        messages = (
            [{"role": "system", "content": self.system_prompt()}]
            + self.clean_history(history)
            + [{"role": "user", "content": message}]
        )
        done = False
        response = None  # Initialize response outside loop

        while not done:
            response = self.llama3_3_groq.chat.completions.create(
                model=self.LLAMA3_3_MODEL, messages=messages, tools=tools
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
        evaluation = self.evaluate(
            response.choices[0].message.content, message, history
        )

        if evaluation.is_acceptable:
            print(f"Passed evaluation from {self.evaluation_model} - returning reply")
            return response.choices[0].message.content
        else:
            print("Failed evaluation - retrying")
            print(evaluation.feedback)
            self.rerun(
                response.choices[0].message.content,
                message,
                history,
                evaluation.feedback,
            )
            return response.choices[0].message.content


if __name__ == "__main__":
    me = Me()

    def log_user_info(message, history, request: gr.Request):
        # Get user information from the request parameter
        if request:
            ip = request.client.host
            user_agent = request.headers.get("User-Agent", "Unknown")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Get location info using ipinfo.io (or use another API if you prefer)
            location = "Unknown"
            try:
                resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("bogon"):
                        location = "Bogon IP Localhost/Private Network"
                    else:
                        city = data.get("city", "")
                        region = data.get("region", "")
                        country = data.get("country", "")
                        location = f"{city}, {region}, {country}".strip(", ")
            except Exception as e:
                print(f"Location lookup failed: {e}", flush=True)

            # Log user information
            print(
                f"[{timestamp}] User Info - IP: {ip}, Location: {location}, User-Agent: {user_agent}",
                flush=True,
            )

        # Call the original chat function
        return me.chat(message, history)

    gr.ChatInterface(fn=log_user_info, type="messages").launch()
