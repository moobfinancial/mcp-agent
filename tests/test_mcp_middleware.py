import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Add the parent directory to sys.path to import modules from the project
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the actual implementation
from mcp.middleware import MCPMiddleware, AuthenticationError, RoutingError

class TestMCPMiddleware(unittest.TestCase):
    """Test suite for MCP Agent Middleware"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Mock configuration for testing
        self.mock_config = {
            "version": "1.0.0",
            "intents": {
                "get_products": {
                    "endpoint": "/api/products",
                    "method": "GET",
                    "description": "Get all products"
                },
                "get_product_detail": {
                    "endpoint": "/api/products/{id}",
                    "method": "GET",
                    "description": "Get product details",
                    "required_params": ["id"]
                }
            },
            "parameters": {
                "id": {
                    "type": "integer",
                    "description": "Product ID"
                }
            },
            "responses": {
                "product_list": {
                    "template": "Found {count} products",
                    "variables": ["count"]
                }
            }
        }
        
        # Initialize the middleware with mock config
        self.middleware = MCPMiddleware(config=self.mock_config)
        
        # Mock request from MCP
        self.mock_mcp_request = {
            "intent": "get_products",
            "parameters": {},
            "token": "mock_valid_token",
            "session_id": "test_session_123"
        }
        
        # Mock API response
        self.mock_api_response = {
            "data": [
                {"id": 1, "name": "Product 1", "price": 19.99},
                {"id": 2, "name": "Product 2", "price": 29.99}
            ],
            "count": 2
        }
    
    @patch('mcp.middleware.requests.get')
    def test_route_request_to_api(self, mock_get):
        """Test that requests are correctly routed to the API"""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_api_response
        mock_get.return_value = mock_response
        
        # Call the middleware
        response = self.middleware.route_request(self.mock_mcp_request)
        
        # Assert the request was routed correctly
        mock_get.assert_called_once_with(
            "http://localhost:8000/api/products",
            headers={"Authorization": "Bearer mock_valid_token", "Content-Type": "application/json"},
            params={}
        )
        
        # Assert the response was processed correctly
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Found 2 products")
        self.assertEqual(response["data"], self.mock_api_response)
    
    def test_authentication_validation(self):
        """Test that authentication is properly validated"""
        # Test with valid token
        valid_request = {
            "intent": "get_products",
            "parameters": {},
            "token": "mock_valid_token",
            "session_id": "test_session_123"
        }
        
        self.assertTrue(self.middleware.validate_authentication(valid_request))
        
        # Test with missing token
        invalid_request = {
            "intent": "get_products",
            "parameters": {},
            "session_id": "test_session_123"
        }
        
        with self.assertRaises(AuthenticationError):
            self.middleware.validate_authentication(invalid_request)
        
        # Test with invalid token format
        invalid_request = {
            "intent": "get_products",
            "parameters": {},
            "token": "inv",  # Too short
            "session_id": "test_session_123"
        }
        
        with self.assertRaises(AuthenticationError):
            self.middleware.validate_authentication(invalid_request)
    
    def test_parameter_extraction(self):
        """Test that parameters are correctly extracted and validated"""
        # Test with required parameter
        request_with_param = {
            "intent": "get_product_detail",
            "parameters": {"id": 123},
            "token": "mock_valid_token",
            "session_id": "test_session_123"
        }
        
        params = self.middleware.extract_parameters(request_with_param)
        self.assertEqual(params["id"], 123)
        
        # Test with missing required parameter
        request_missing_param = {
            "intent": "get_product_detail",
            "parameters": {},
            "token": "mock_valid_token",
            "session_id": "test_session_123"
        }
        
        with self.assertRaises(RoutingError):
            self.middleware.extract_parameters(request_missing_param)
    
    def test_response_formatting(self):
        """Test that API responses are correctly formatted for MCP"""
        formatted_response = self.middleware.format_response(
            "get_products", 
            self.mock_api_response
        )
        
        self.assertEqual(formatted_response["status"], "success")
        self.assertEqual(formatted_response["message"], "Found 2 products")
        self.assertEqual(formatted_response["data"], self.mock_api_response)
    
    def test_error_handling(self):
        """Test that errors are properly handled and formatted"""
        # Mock API error response
        error_response = {
            "detail": "Product not found"
        }
        
        formatted_error = self.middleware.handle_error(404, error_response)
        
        self.assertEqual(formatted_error["status"], "error")
        self.assertEqual(formatted_error["code"], 404)
        self.assertTrue("not found" in formatted_error["message"].lower())

if __name__ == '__main__':
    unittest.main()
