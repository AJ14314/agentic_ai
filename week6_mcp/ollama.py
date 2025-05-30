# Cell 1: Setup
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import os
import nest_asyncio
nest_asyncio.apply()

# Cell 2: Load environment variables
load_dotenv(override=True)

# Cell 3: Define tool fetcher
async def get_tools(params):
    async with MCPServerStdio(params=params) as server:
        tools = await server.list_tools()
    for tool in tools:
        print(f"{tool.name}: {tool.description.replace('\n', ' ')}")
    return tools

# Cell 4: Setup tool parameters
sandbox_path = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))
print(f"sandbox_path: {sandbox_path}")

puppeteer_params = {
    "command": "/home/anand/.nvm/versions/node/v24.1.0/bin/npx",
    "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
}

files_params = {
    "command": "/home/anand/.nvm/versions/node/v24.1.0/bin/npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]
}

playwright_params = {
    "command": "/home/anand/.nvm/versions/node/v24.1.0/bin/npx",
    "args": ["-y", "@playwright/mcp@latest"]  # Use latest version
}

# Cell 5: Create LLM client
from agents import OpenAIChatCompletionsModel, AsyncOpenAI

llm_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

llm_model = OpenAIChatCompletionsModel(
    model="llama3.2:3b",  # Correct model name
    openai_client=llm_client
)

# Cell 6: Run agent with tools
async def run_agent():
    instructions = """
    You browse the internet to accomplish your instructions.
    You are highly capable at browsing the internet independently to accomplish your task,
    including accepting all cookies and clicking 'not now' as appropriate to get to the content you need.
    If one website isn't fruitful, try another. Be persistent until you have solved your assignment,
    trying different options and sites as needed.
    """

    async with MCPServerStdio(params=files_params, cache_tools_list=False) as mcp_server_files:
        async with MCPServerStdio(params=playwright_params, cache_tools_list=False) as mcp_server_browser:
            print("Starting agent...")
            agent = Agent(
                name="investigator",
                instructions=instructions,
                model=llm_model,
                mcp_servers=[mcp_server_files, mcp_server_browser],
            )
            with trace("investigate"):
                result = await Runner.run(
                    agent,
                    "Find a great recipe for Banoffee Pie, then summarize it in markdown to banoffee2.md"
                )
                print(result.final_output)

# Run the agent
import asyncio
asyncio.run(run_agent())