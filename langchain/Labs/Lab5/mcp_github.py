import os
import requests
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
import asyncio
from dotenv import load_dotenv
from fastmcp import Client
from langchain.tools import tool
from fastmcp.client.transports import StdioTransport

# Load environment variables from .env file
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

# Async function to call MCP server's list_commits tool
async def list_commits(owner: str, repo: str, page: str = None, per_page: str = None, sha: str = None) -> list:
    transport = StdioTransport(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")},
    )
    client = Client(transport)
    async with client:
        params = {"owner": owner, "repo": repo}
        if page:
            params["page"] = int(page)
        if per_page:
            params["per_page"] = int(per_page)
        if sha:
            params["sha"] = sha
        result = await client.call_tool("list_commits", params)
        if result.content:
            return result.content
        else:
            raise ValueError(f"No commit data returned for params: {params}")

@tool
def get_commit_list(owner: str, repo: str, page: str = None, per_page: str = None, sha: str = None) -> list:
    """Fetch commit list using MCP server."""
    return asyncio.run(list_commits(owner, repo, page, per_page, sha))


# Python code to use the MCP server's list_commits tool

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_commit_list]
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=False)

# In Jupyter, you can do:
result = agent.run("List latest commits from main branch of gopalkrushnapattanaik/genaicoding")
print(result)
