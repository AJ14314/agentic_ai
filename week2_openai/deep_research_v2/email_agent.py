import os
from typing import Dict

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool
from groq_client import get_groq_model

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send out an email with the given body to the recipients"""
    sg = SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = Email(
        "anandjain14314_automation.bsojl@slmail.me"
    )
    to_email = To("anandjain14314@gmail.com")
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.send(mail)
    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=get_groq_model(),
)
