# MCP Proof-of-Concept: AI Agent to Backend Integration

> Created: 2025-05-01

This project demonstrates a proof-of-concept for using the Model Context Protocol (MCP) to connect AI agents to a backend application. It enables an AI agent to discover and call backend functions exposed through a FastAPI service.

## What is MCP?

The Model Context Protocol (MCP) is a standardized protocol that allows AI models (like LLMs) to interact with application functions ("tools") in a consistent way. It's the bridge between AI agents and backend business logic.

## Project Components

- **FastAPI Backend**: Exposes product information APIs
- **MCP Integration**: Uses `fastapi-mcp` to expose FastAPI endpoints as callable tools
- **AI Agent**: Python script using `mcp-use` to connect an LLM to the MCP server
- **Database Layer**: Placeholder SQLAlchemy implementation (using SQLite for development)

## Prerequisites

- Python 3.8+
- OpenAI API key (for GPT-4o access)

## Installation

1. Clone this repository
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:

```bash
cp .env.example .env
# Edit .env to add your actual OpenAI API key
```

## Running the Project

### Start the FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

The backend will start at http://127.0.0.1:8000 with:
- API documentation: http://127.0.0.1:8000/docs
- MCP server: http://127.0.0.1:8000/mcp
- MCP SSE endpoint: http://127.0.0.1:8000/mcp/sse

### Run the AI Agent

In a separate terminal (with the virtual environment activated):

```bash
python agent/agent_script.py
```

The agent will:
1. Connect to the running MCP server
2. Use GPT-4o to understand and select the appropriate tool
3. Call the backend product retrieval endpoint via MCP
4. Process and display the results

## Project Structure

```
mcp_poc/
├── agent/                  # AI agent using mcp-use
│   └── agent_script.py
├── backend/                # FastAPI application
│   ├── db/                 # Database layer
│   │   ├── crud.py         # Database operations  
│   │   ├── database.py     # SQLAlchemy setup
│   │   └── models.py       # Data models
│   ├── __init__.py
│   └── main.py             # FastAPI app with MCP integration
├── venv/                   # Virtual environment (git-ignored)
├── .env                    # Environment variables (git-ignored)
├── .env.example            # Template for .env
├── Build_Plan.md           # Project task checklist
├── changelog.md            # Version history
├── README.md               # This file
└── requirements.txt        # Project dependencies
```

## How It Works

1. The FastAPI backend defines endpoints for retrieving product information.
2. `fastapi-mcp` exposes these endpoints as MCP tools.
3. The agent script uses `mcp-use` and GPT-4o to:
   - Parse natural language requests ("get info about product 1")
   - Identify which tool to call
   - Format arguments correctly
   - Call the tool via the MCP protocol
4. The MCP server routes the call to the corresponding FastAPI endpoint.
5. The endpoint processes the request and returns the product data.
6. The agent receives and displays the result.

## Authentication

The project implements standard Bearer token authentication:

1. **Backend Security**: The FastAPI backend uses OAuth2-compatible Bearer token security via `HTTPBearer` dependency.

2. **Agent Authorization**: The agent script sends authentication tokens via the `Authorization` header in the MCP configuration:
   ```python
   config = {
       "mcpServers": {
           "server_name": {
               "url": "http://127.0.0.1:8000/mcp",
               "headers": {
                   "Authorization": "Bearer your-api-key"
               }
           }
       }
   }
   ```

3. **Production Considerations**: 
   - In a production environment, use JWT tokens with proper expiration and signing
   - Store tokens in environment variables, not in source code
   - Consider implementing refresh token flows for long-running agents

## Next Steps

- ✅ Integrate with a real PostgreSQL database
- ✅ Add authentication to the endpoints
- Create a simple React frontend that uses the AI agent
- Deploy to a production environment

## Technologies

- [FastAPI](https://fastapi.tiangolo.com/): High-performance API framework
- [MCP](https://github.com/context7/mcp): Model Context Protocol
- [fastapi-mcp](https://github.com/context7/fastapi-mcp): MCP integration for FastAPI
- [mcp-use](https://github.com/context7/mcp-use): MCP client for AI agents
- [LangChain](https://python.langchain.com/): Framework for LLM applications
- [SQLAlchemy](https://www.sqlalchemy.org/): SQL toolkit and ORM
