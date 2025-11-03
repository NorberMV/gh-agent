# MCP Agents

Multi-agent system using MCP (Model Context Protocol) servers with LangChain.

## Agents

### GitHub Agent (Default)
A ReAct agent using MCP GitHub server tools for repository management, issues, and workflows.

### Podcast Agent
A ReAct agent using Audioscrape MCP server to search over 1 million hours of audio content including podcasts, interviews, and conversations.

### Articles Search Agent
A ReAct agent that researches recent web articles and news about founders. Uses Dappier and Serper Search MCP servers for comprehensive article searching, Fetch MCP server to retrieve content and metadata from article URLs, and favicon-generator for image processing. Returns article information with title, date, description, and image URLs.

## Setup

1. Copy `example.env` to `.env` and fill in your API keys:
   ```bash
   cp example.env .env
   ```

2. **Get API Keys** (required for some agents):
   - **Audioscrape API Key** (required for podcast agent):
     - Visit [https://mcp.audioscrape.com](https://mcp.audioscrape.com) to register and obtain your API key
     - Add it to your `.env` file:
       ```
       AUDIOSCRAPE_API_KEY=your_actual_api_key_here
       ```
   - **Dappier API Key** (required for articles search agent):
     - Get your Dappier API key from [Dappier](https://dappier.com) or your Dappier account
     - Add it to your `.env` file:
       ```
       DAPPIER_API_KEY=your_actual_api_key_here
       ```
   - **Serper API Key** (required for articles search agent):
     - Get your Serper API key from [Serper.dev](https://serper.dev) - a Google Search API
     - Add it to your `.env` file:
       ```
       SERPER_API_KEY=your_actual_api_key_here
       ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run GitHub Agent (Default)
```bash
python mcp_client.py
```

### Run Podcast Agent
```bash
# With default query
python mcp_client.py podcast

# With custom query
python mcp_client.py podcast "Search for podcast episodes about AI safety"
```

### Run Articles Search Agent
```bash
# With default query (searches for articles about Elon Musk)
python mcp_client.py articles

# Search for articles about a specific founder
python mcp_client.py articles "Sam Altman"

# With a full query
python mcp_client.py articles "Research recent articles about Jensen Huang"
```

## Configuration

Edit `mcp_config.json` to configure MCP servers:
- `github-mcp-server`: GitHub MCP server (Docker)
- `dappier`: Dappier MCP server for article searching
- `audioscrape`: Audioscrape HTTP MCP server for podcast search
- `favicon-generator`: Favicon generator MCP server for creating website favicons
- `serper-search`: Serper Search MCP server for Google Search API-based article searching
- `fetch`: Fetch MCP server (Docker) for retrieving content and metadata from URLs
