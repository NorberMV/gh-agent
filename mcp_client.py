import os
import asyncio
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent

from tools import think_tool
from prompts import GITHUB_AGENT_SYSTEM_MESSAGE
from utils import read_config

from dotenv import load_dotenv

load_dotenv()


GH_PAT = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
config_file_path = Path(__file__).parent.resolve() / "mcp_config.json"


async def main():

    mcp_servers = read_config(config_file_path)
    mcp_servers["github-mcp-server"]["env"]["GITHUB_PERSONAL_ACCESS_TOKEN"] = GH_PAT

    client = MultiServerMCPClient(
        mcp_servers,
    )

    tools = await client.get_tools()  
    tools.append(think_tool)
    print(f"The available tools are: {len(tools)}")

    agent = create_agent(
        "claude-sonnet-4-5-20250929",
        system_prompt=GITHUB_AGENT_SYSTEM_MESSAGE,
        tools=tools,
    )

    gh_agent_response = await agent.ainvoke(
        {
            "messages": 
            [
                {
                    "role": "user", 
                    # "content": "Search for podcasts episodes of Elon Musk on AI the last month",
                    "content": """Could you check what I've been working lately on the agentic-ai-with-python-specialization repo? 
                    I want to understand what I've been working on lately. So collect information about all my recent activity 
                    and provide a brief overview in natural human language about my recent work.""",
                }
            ]
        }
    )

    print(f"The response is:")

    for message in gh_agent_response["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())