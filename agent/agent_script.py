"""Simple MCP agent that queries the FastAPI backend.

Usage:
    python agent/agent_script.py

Ensure the FastAPI backend is running locally first:
    uvicorn backend.main:app --reload
"""
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient


async def main():
    load_dotenv()

    # Try the standard MCP endpoint first
    # If that doesn't work, we'll modify to use the correct one
    fastapi_mcp_server_url = "http://127.0.0.1:8000/mcp"

    config = {
        "mcpServers": {
            "ecommerce_backend": {
                "url": fastapi_mcp_server_url,
            }
        }
    }

    client = MCPClient.from_dict(config)

    llm = ChatOpenAI(model="gpt-4o")

    agent = MCPAgent(llm=llm, client=client, max_steps=20)

    query = "Tell me about product 1"
    print(f"Running agent query: {query}\n")

    result = await agent.run(query)

    print("\n--- Agent Result ---")
    print(result)

    await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(main())
