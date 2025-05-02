"""Simple MCP agent that queries the FastAPI backend.

Usage:
    python agent/agent_script.py

Ensure the FastAPI backend is running locally first:
    uvicorn backend.main:app --reload
"""
import asyncio
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    load_dotenv()

    # Using the MCP endpoint URL with proper authorization headers
    fastapi_mcp_server_url = "http://127.0.0.1:8000/mcp"
    
    logger.info(f"Connecting to MCP server at: {fastapi_mcp_server_url}")
    
    # Add authentication token as recommended in the documentation
    # Using authorization header approach which is the recommended default
    auth_token = "Bearer test-api-key"  # In production, this would come from env var
    logger.info(f"Setting Authorization header: {auth_token}")
    
    config = {
        "mcpServers": {
            "ecommerce_backend": {
                "url": fastapi_mcp_server_url,
                "headers": {
                    "Authorization": auth_token
                }
            }
        }
    }

    try:
        client = MCPClient.from_dict(config)
        
        llm = ChatOpenAI(model="gpt-4o")
        logger.info("LLM initialized")
        
        agent = MCPAgent(llm=llm, client=client, max_steps=20, verbose=True)
        logger.info("Agent created")
        
        # Try a direct product ID lookup which worked previously
        query = "Tell me about product 1"
        logger.info(f"Running agent query: {query}")
        
        result = await agent.run(query)
        
        print("\n--- Agent Result ---")
        print(result)
        
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            await client.close_all_sessions()
            logger.info("Closed client sessions")


if __name__ == "__main__":
    asyncio.run(main())
