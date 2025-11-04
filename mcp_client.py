import json
import os
import asyncio
import sys
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from tools import think_tool
from prompts import GITHUB_AGENT_SYSTEM_MESSAGE, PODCAST_AGENT_SYSTEM_MESSAGE, ARTICLES_SEARCH_AGENT_SYSTEM_MESSAGE
from utils import read_config
from models import ArticlesItems, PodcastItems

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


async def old_create_podcast_agent():
    """Create a separate agent for the Audioscrape podcast server."""
    config_file_path = Path(__file__).parent.resolve() / "mcp_config.json"
    
    # Read all servers but only use audioscrape
    all_servers = read_config(config_file_path)
    podcast_servers = {"audioscrape": all_servers["audioscrape"]}
    
    # Set up authentication if API key is provided
    audioscrape_api_key = os.environ.get("AUDIOSCRAPE_API_KEY")
    if audioscrape_api_key:
        # Format as Bearer token if not already formatted
        if not audioscrape_api_key.startswith("Bearer "):
            bearer_token = f"Bearer {audioscrape_api_key}"
        else:
            bearer_token = audioscrape_api_key
        
        # Update headers with authentication
        if "headers" in podcast_servers["audioscrape"]:
            podcast_servers["audioscrape"]["headers"]["Authorization"] = bearer_token
        else:
            podcast_servers["audioscrape"]["headers"] = {"Authorization": bearer_token}
    else:
        print("⚠️  Warning: AUDIOSCRAPE_API_KEY not found in environment variables.")
        print("   The server may require authentication. Visit https://mcp.audioscrape.com for API key registration.")
    
    client = MultiServerMCPClient(podcast_servers)
    
    # Get tools from the audioscrape server
    tools = await client.get_tools()
    tools.append(think_tool)
    print(f"Podcast agent tools available: {len(tools)}")
    
    # Create the agent with podcast-specific prompt
    agent = create_agent(
        "claude-sonnet-4-5-20250929",
        system_prompt=PODCAST_AGENT_SYSTEM_MESSAGE,
        tools=tools,
    )
    
    return agent


async def create_podcast_agent():
    """Create a separate agent for podcast searching using serper-search server."""
    config_file_path = Path(__file__).parent.resolve() / "mcp_config.json"
    
    # Read all servers and use serper-search
    all_servers = read_config(config_file_path)
    podcast_servers = {
        "serper-search": all_servers["serper-search"]
    }
    
    # Set up authentication for serper-search if API key is provided
    serper_api_key = os.environ.get("SERPER_API_KEY")
    if serper_api_key:
        podcast_servers["serper-search"]["env"]["SERPER_API_KEY"] = serper_api_key
    else:
        print("⚠️  Warning: SERPER_API_KEY not found in environment variables.")
        print("   The serper-search server may require authentication.")
    
    client = MultiServerMCPClient(podcast_servers)
    
    # Get tools from serper-search server (google_search, scrape)
    tools = await client.get_tools()
    tools.append(think_tool)
    print(f"Podcast agent tools available: {len(tools)}")
    
    # Create the agent with podcast-specific prompt
    agent = create_agent(
        "google_genai:gemini-2.5-pro",
        system_prompt=PODCAST_AGENT_SYSTEM_MESSAGE,
        tools=tools,
        response_format=ToolStrategy(PodcastItems),
    )
    
    return agent

async def run_podcast_agent():
    """Run the podcast agent with a sample query."""
    podcast_agent = await create_podcast_agent()
    
    # Example query - you can modify this or pass it as an argument
    query = "Search for podcast episodes of Elon Musk on AI from the last month"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    
    print(f"\n🔍 Podcast Agent Query: {query}\n")
    
    response = await podcast_agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": query
        }]
    })
    
    print(f"\n📻 Podcast Agent Response:\n")
    for message in response["messages"]:
        message.pretty_print()
    
    result = response["structured_response"]
    podcasts_list = result.model_dump()
    print(json.dumps(podcasts_list, indent=4))


async def create_articles_agent():
    """Create a separate agent for article searching using serper-search, fetch, and favicon-generator servers."""
    config_file_path = Path(__file__).parent.resolve() / "mcp_config.json"
    
    # Read all servers and use serper-search, fetch, and favicon-generator
    all_servers = read_config(config_file_path)
    article_servers = {
        "serper-search": all_servers["serper-search"],
        "fetch": all_servers["fetch"],
        "favicon-generator": all_servers["favicon-generator"]
    }
    
    # Set up authentication for serper-search if API key is provided
    serper_api_key = os.environ.get("SERPER_API_KEY")
    if serper_api_key:
        article_servers["serper-search"]["env"]["SERPER_API_KEY"] = serper_api_key
    else:
        print("⚠️  Warning: SERPER_API_KEY not found in environment variables.")
        print("   The serper-search server may require authentication.")
    
    client = MultiServerMCPClient(article_servers)
    
    # Get tools from all three servers (serper-search, fetch, favicon-generator)
    tools = await client.get_tools()
    tools.append(think_tool)
    print(f"Articles search agent tools available: {len(tools)}")
    
    # Create the agent with articles search-specific prompt
    agent = create_agent(
        # "claude-sonnet-4-5-20250929",
        "google_genai:gemini-2.5-pro",
        system_prompt=ARTICLES_SEARCH_AGENT_SYSTEM_MESSAGE,
        tools=tools,
        response_format=ToolStrategy(ArticlesItems),
    )
    
    return agent


async def run_articles_agent():
    """Run the articles search agent with a founder name query."""
    articles_agent = await create_articles_agent()
    
    # Example query - you can modify this or pass it as an argument
    query = "Research recent articles about Elon Musk"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    
    # Format the query to ensure it's about researching articles for a founder
    if not any(keyword in query.lower() for keyword in ["research", "articles", "news", "about"]):
        query = f"Research recent articles and news about {query}"
    
    print(f"\n📰 Articles Search Agent Query: {query}\n")
    
    response = await articles_agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": query
        }]
    })
    
    print(f"\n📄 Articles Search Agent Response:\n")
    for message in response["messages"]:
        message.pretty_print()

    result = response["structured_response"]
    articles_list = result.model_dump()
    print(json.dumps(articles_list, indent=4))

if __name__ == "__main__":
    # Check which agent the user wants to run
    if len(sys.argv) > 1 and sys.argv[1] == "podcast":
        # Remove "podcast" from args and pass remaining as query
        sys.argv.pop(1)
        asyncio.run(run_podcast_agent())
    elif len(sys.argv) > 1 and sys.argv[1] == "articles":
        # Remove "articles" from args and pass remaining as query
        sys.argv.pop(1)
        asyncio.run(run_articles_agent())
    else:
        # Run GitHub agent by default
        asyncio.run(main())