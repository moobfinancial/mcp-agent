import json
import os
import re
import logging
import requests
from typing import Dict, Any, List, Optional, Union

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_middleware")

class AuthenticationError(Exception):
    """Exception raised for authentication errors."""
    pass

class RoutingError(Exception):
    """Exception raised for routing errors."""
    pass

class ConfigurationError(Exception):
    """Exception raised for configuration errors."""
    pass

class MCPMiddleware:
    """
    Middleware for handling communication between MCP agent and API endpoints.
    
    This middleware is responsible for:
    1. Authenticating requests from the MCP agent
    2. Routing requests to the appropriate API endpoint
    3. Formatting API responses for the MCP agent
    4. Handling errors and providing meaningful feedback
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, config_path: Optional[str] = None, api_base_url: str = None):
        """
        Initialize the MCP middleware.
        
        Args:
            config: Configuration dictionary (optional)
            config_path: Path to configuration file (optional)
            api_base_url: Base URL for API endpoints (default: http://localhost:8000)
        """
        self.config = config
        self.api_base_url = api_base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        
        if config is None and config_path is None:
            # Default config path
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                      'config', 'mcp_agent_config.json')
        
        if config is None:
            try:
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                raise ConfigurationError(f"Failed to load configuration: {str(e)}")
        
        # Validate the configuration
        self._validate_config()
        
        logger.info(f"MCP Middleware initialized with API base URL: {self.api_base_url}")
    
    def _validate_config(self) -> None:
        """Validate the configuration structure."""
        required_sections = ["version", "intents", "parameters", "responses"]
        for section in required_sections:
            if section not in self.config:
                raise ConfigurationError(f"Missing required section '{section}' in configuration")
        
        # Validate intents
        for intent_name, intent_config in self.config["intents"].items():
            if "endpoint" not in intent_config or "method" not in intent_config:
                raise ConfigurationError(f"Intent '{intent_name}' missing required fields")
    
    def validate_authentication(self, request: Dict[str, Any]) -> bool:
        """
        Validate the authentication token in the request.
        
        Args:
            request: Request from MCP agent
            
        Returns:
            bool: True if authentication is valid
            
        Raises:
            AuthenticationError: If authentication is invalid
        """
        if "token" not in request:
            raise AuthenticationError("Missing authentication token")
        
        token = request["token"]
        
        # Basic validation of token format
        if not token or not isinstance(token, str) or len(token) < 10:
            raise AuthenticationError("Invalid token format")
        
        # In a real implementation, we would validate the token with the auth service
        # For now, we'll just check if it starts with "mock_valid_" for testing
        if token.startswith("mock_valid_"):
            return True
        
        # TODO: Implement actual token validation with auth service
        logger.warning("Using simplified token validation. Replace with actual validation in production.")
        return True
    
    def extract_parameters(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and validate parameters from the request.
        
        Args:
            request: Request from MCP agent
            
        Returns:
            Dict[str, Any]: Extracted parameters
            
        Raises:
            RoutingError: If required parameters are missing or invalid
        """
        intent = request.get("intent")
        if not intent or intent not in self.config["intents"]:
            raise RoutingError(f"Invalid or missing intent: {intent}")
        
        intent_config = self.config["intents"][intent]
        params = request.get("parameters", {})
        
        # Check required parameters
        required_params = intent_config.get("required_params", [])
        for param in required_params:
            if param not in params:
                raise RoutingError(f"Missing required parameter: {param}")
        
        # Validate parameter types
        for param_name, param_value in params.items():
            if param_name in self.config["parameters"]:
                param_config = self.config["parameters"][param_name]
                param_type = param_config["type"]
                
                # Basic type validation
                if param_type == "integer" and not isinstance(param_value, int):
                    raise RoutingError(f"Parameter '{param_name}' must be an integer")
                elif param_type == "number" and not isinstance(param_value, (int, float)):
                    raise RoutingError(f"Parameter '{param_name}' must be a number")
                elif param_type == "string" and not isinstance(param_value, str):
                    raise RoutingError(f"Parameter '{param_name}' must be a string")
                elif param_type == "boolean" and not isinstance(param_value, bool):
                    raise RoutingError(f"Parameter '{param_name}' must be a boolean")
                elif param_type == "array" and not isinstance(param_value, list):
                    raise RoutingError(f"Parameter '{param_name}' must be an array")
                elif param_type == "object" and not isinstance(param_value, dict):
                    raise RoutingError(f"Parameter '{param_name}' must be an object")
                
                # Advanced validation if specified
                if "validation" in param_config:
                    validation_rule = param_config["validation"]
                    # Simple validation using eval (in production, use a safer approach)
                    # Replace 'value' with the actual parameter value
                    validation_code = validation_rule.replace("value", str(param_value))
                    try:
                        if not eval(validation_code):
                            raise RoutingError(f"Parameter '{param_name}' failed validation: {validation_rule}")
                    except Exception as e:
                        raise RoutingError(f"Error validating parameter '{param_name}': {str(e)}")
        
        return params
    
    def _build_url(self, endpoint: str, params: Dict[str, Any]) -> str:
        """
        Build the URL for the API request, replacing path parameters.
        
        Args:
            endpoint: API endpoint path
            params: Request parameters
            
        Returns:
            str: Full URL with path parameters replaced
        """
        # Replace path parameters (e.g., {id} -> 123)
        path_params = re.findall(r'\{(\w+)\}', endpoint)
        url = endpoint
        
        for param in path_params:
            if param in params:
                url = url.replace(f"{{{param}}}", str(params[param]))
                # Remove the parameter from the query params since it's in the path
                params.pop(param, None)
        
        return f"{self.api_base_url}{url}"
    
    def route_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route the request to the appropriate API endpoint.
        
        Args:
            request: Request from MCP agent
            
        Returns:
            Dict[str, Any]: Response from API
            
        Raises:
            AuthenticationError: If authentication is invalid
            RoutingError: If routing fails
        """
        # Validate authentication
        self.validate_authentication(request)
        
        # Extract intent and parameters
        intent = request.get("intent")
        if not intent or intent not in self.config["intents"]:
            raise RoutingError(f"Invalid or missing intent: {intent}")
        
        intent_config = self.config["intents"][intent]
        endpoint = intent_config["endpoint"]
        method = intent_config["method"]
        
        # Extract and validate parameters
        params = self.extract_parameters(request)
        
        # Build the URL
        url = self._build_url(endpoint, params)
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {request['token']}",
            "Content-Type": "application/json"
        }
        
        # Make the request to the API
        try:
            logger.info(f"Routing request to {method} {url}")
            
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=params)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=params)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, params=params)
            else:
                raise RoutingError(f"Unsupported HTTP method: {method}")
            
            # Check for errors
            if response.status_code >= 400:
                return self.handle_error(response.status_code, response.json())
            
            # Format the response
            api_response = response.json()
            return self.format_response(intent, api_response)
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return self.handle_error(500, {"detail": f"API request failed: {str(e)}"})
    
    def format_response(self, intent: str, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the API response for the MCP agent.
        
        Args:
            intent: The intent that was processed
            api_response: Response from the API
            
        Returns:
            Dict[str, Any]: Formatted response for MCP agent
        """
        # Determine which response template to use
        response_type = None
        if intent == "get_products":
            response_type = "product_list"
        elif intent == "get_product_detail":
            response_type = "product_detail"
        elif intent == "create_order":
            response_type = "order_confirmation"
        elif intent == "get_user_profile" or intent == "update_user_profile":
            response_type = "user_profile"
        else:
            # Default to a generic response
            return {
                "status": "success",
                "data": api_response
            }
        
        # Get the response template
        if response_type in self.config["responses"]:
            template = self.config["responses"][response_type]["template"]
            variables = self.config["responses"][response_type].get("variables", [])
            
            # Replace variables in the template
            message = template
            for var in variables:
                if var in api_response:
                    message = message.replace(f"{{{var}}}", str(api_response[var]))
            
            return {
                "status": "success",
                "message": message,
                "data": api_response
            }
        
        # Fallback to returning the raw response
        return {
            "status": "success",
            "data": api_response
        }
    
    def handle_error(self, status_code: int, error_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle and format error responses.
        
        Args:
            status_code: HTTP status code
            error_response: Error response from API
            
        Returns:
            Dict[str, Any]: Formatted error response for MCP agent
        """
        error_detail = error_response.get("detail", "Unknown error")
        
        # Map status codes to error types
        if status_code == 404:
            response_type = "error_not_found"
            resource = "resource"  # Default value
            
            # Try to extract resource type from error message
            if isinstance(error_detail, str):
                if "product" in error_detail.lower():
                    resource = "product"
                elif "user" in error_detail.lower():
                    resource = "user"
                elif "order" in error_detail.lower():
                    resource = "order"
            
            if response_type in self.config["responses"]:
                template = self.config["responses"][response_type]["template"]
                message = template.replace("{resource}", resource)
            else:
                message = f"Resource not found: {error_detail}"
                
        elif status_code == 400 or status_code == 422:
            response_type = "error_validation"
            
            if response_type in self.config["responses"]:
                template = self.config["responses"][response_type]["template"]
                message = template.replace("{error_message}", str(error_detail))
            else:
                message = f"Validation error: {error_detail}"
                
        else:
            # Generic error message
            message = f"Error {status_code}: {error_detail}"
        
        logger.error(f"API error: {status_code} - {error_detail}")
        
        return {
            "status": "error",
            "code": status_code,
            "message": message,
            "details": error_response
        }
