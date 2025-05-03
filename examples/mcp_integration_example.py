#!/usr/bin/env python3
"""
Example script demonstrating how to use the MCP middleware with API endpoints.

This script shows how to:
1. Initialize the MCP middleware with a configuration
2. Process requests from the MCP agent
3. Route requests to API endpoints
4. Format responses for the MCP agent

Usage:
    python mcp_integration_example.py
"""

import os
import sys
import json
import logging
from typing import Dict, Any

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.middleware import MCPMiddleware, AuthenticationError, RoutingError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_example")

def simulate_mcp_request(intent: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Simulate a request from the MCP agent.
    
    Args:
        intent: The intent to process
        params: Parameters for the intent
        
    Returns:
        Dict[str, Any]: Simulated MCP request
    """
    return {
        "intent": intent,
        "parameters": params or {},
        "token": "mock_valid_token",
        "session_id": "example_session_123"
    }

def main():
    """Main function demonstrating MCP middleware usage."""
    logger.info("Initializing MCP middleware...")
    
    # Initialize the middleware with the default configuration
    middleware = MCPMiddleware()
    
    # Example 1: Get all products
    logger.info("\n\nExample 1: Get all products")
    try:
        request = simulate_mcp_request("get_products")
        logger.info(f"Processing request: {json.dumps(request, indent=2)}")
        
        # In a real scenario, this would make an actual API call
        # For this example, we'll mock the response in the test
        response = middleware.route_request(request)
        logger.info(f"Response: {json.dumps(response, indent=2)}")
    except (AuthenticationError, RoutingError) as e:
        logger.error(f"Error processing request: {str(e)}")
    
    # Example 2: Get product detail
    logger.info("\n\nExample 2: Get product detail")
    try:
        request = simulate_mcp_request("get_product_detail", {"id": 123})
        logger.info(f"Processing request: {json.dumps(request, indent=2)}")
        
        response = middleware.route_request(request)
        logger.info(f"Response: {json.dumps(response, indent=2)}")
    except (AuthenticationError, RoutingError) as e:
        logger.error(f"Error processing request: {str(e)}")
    
    # Example 3: Create an order
    logger.info("\n\nExample 3: Create an order")
    try:
        order_items = [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ]
        request = simulate_mcp_request("create_order", {"order_items": order_items})
        logger.info(f"Processing request: {json.dumps(request, indent=2)}")
        
        response = middleware.route_request(request)
        logger.info(f"Response: {json.dumps(response, indent=2)}")
    except (AuthenticationError, RoutingError) as e:
        logger.error(f"Error processing request: {str(e)}")
    
    # Example 4: Error handling (missing required parameter)
    logger.info("\n\nExample 4: Error handling (missing required parameter)")
    try:
        request = simulate_mcp_request("get_product_detail", {})  # Missing 'id'
        logger.info(f"Processing request: {json.dumps(request, indent=2)}")
        
        response = middleware.route_request(request)
        logger.info(f"Response: {json.dumps(response, indent=2)}")
    except RoutingError as e:
        logger.error(f"Error processing request: {str(e)}")

if __name__ == "__main__":
    main()
