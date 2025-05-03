import unittest
import json
import os
import jsonschema
from jsonschema import validate

class TestMCPAgentConfig(unittest.TestCase):
    """Test suite for MCP Agent Configuration file"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Define the expected path to the configuration file
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                        'config', 'mcp_agent_config.json')
        
        # Define the expected schema for the configuration file
        self.config_schema = {
            "type": "object",
            "required": ["version", "intents", "parameters", "responses"],
            "properties": {
                "version": {"type": "string"},
                "intents": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "required": ["endpoint", "method", "description"],
                        "properties": {
                            "endpoint": {"type": "string"},
                            "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"]},
                            "description": {"type": "string"},
                            "required_params": {"type": "array", "items": {"type": "string"}},
                            "optional_params": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "parameters": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "required": ["type", "description"],
                        "properties": {
                            "type": {"type": "string", "enum": ["string", "integer", "number", "boolean", "array", "object"]},
                            "description": {"type": "string"},
                            "default": {},
                            "validation": {"type": "string"}
                        }
                    }
                },
                "responses": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "required": ["template"],
                        "properties": {
                            "template": {"type": "string"},
                            "variables": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                }
            }
        }
    
    def test_config_file_exists(self):
        """Test that the configuration file exists"""
        self.assertTrue(os.path.exists(self.config_path), 
                        f"Configuration file not found at {self.config_path}")
    
    def test_config_file_is_valid_json(self):
        """Test that the configuration file is valid JSON"""
        try:
            with open(self.config_path, 'r') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.fail(f"Configuration file is not valid JSON: {str(e)}")
    
    def test_config_schema_validation(self):
        """Test that the configuration file adheres to the expected schema"""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        try:
            validate(instance=config, schema=self.config_schema)
        except jsonschema.exceptions.ValidationError as e:
            self.fail(f"Configuration file does not match schema: {str(e)}")
    
    def test_required_intents_exist(self):
        """Test that all required intents are defined in the configuration"""
        required_intents = [
            "get_products", 
            "get_product_detail", 
            "create_order",
            "get_user_profile",
            "update_user_profile"
        ]
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        for intent in required_intents:
            self.assertIn(intent, config["intents"], 
                          f"Required intent '{intent}' not found in configuration")
    
    def test_intent_endpoint_mapping(self):
        """Test that intents correctly map to API endpoints"""
        expected_mappings = {
            "get_products": {"endpoint": "/api/products", "method": "GET"},
            "get_product_detail": {"endpoint": "/api/products/{id}", "method": "GET"},
            "create_order": {"endpoint": "/api/orders", "method": "POST"},
            "get_user_profile": {"endpoint": "/api/user/profile", "method": "GET"},
            "update_user_profile": {"endpoint": "/api/user/profile", "method": "PUT"}
        }
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        for intent, mapping in expected_mappings.items():
            self.assertIn(intent, config["intents"], 
                          f"Intent '{intent}' not found in configuration")
            self.assertEqual(config["intents"][intent]["endpoint"], mapping["endpoint"],
                            f"Endpoint for intent '{intent}' does not match expected value")
            self.assertEqual(config["intents"][intent]["method"], mapping["method"],
                            f"Method for intent '{intent}' does not match expected value")
    
    def test_parameter_definitions(self):
        """Test that all parameters have proper definitions"""
        required_parameters = [
            "product_id", 
            "user_id", 
            "order_items",
            "quantity",
            "price"
        ]
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        for param in required_parameters:
            self.assertIn(param, config["parameters"], 
                          f"Required parameter '{param}' not defined in configuration")
            self.assertIn("type", config["parameters"][param], 
                          f"Parameter '{param}' missing type definition")
            self.assertIn("description", config["parameters"][param], 
                          f"Parameter '{param}' missing description")
    
    def test_response_templates(self):
        """Test that response templates are properly defined"""
        required_responses = [
            "product_list", 
            "product_detail", 
            "order_confirmation",
            "user_profile",
            "error_not_found",
            "error_validation"
        ]
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        for response in required_responses:
            self.assertIn(response, config["responses"], 
                          f"Required response '{response}' not defined in configuration")
            self.assertIn("template", config["responses"][response], 
                          f"Response '{response}' missing template definition")

if __name__ == '__main__':
    unittest.main()
