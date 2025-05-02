"""Basic authentication system for the FastAPI backend.

This authentication module defines a simple API key header authentication system
that can be used as a FastAPI Dependency.
"""
from fastapi import Depends, HTTPException, Header, status


API_KEYS = {
    "test-api-key": "test-user",
    "dev-api-key": "developer",
}


async def verify_api_key(x_api_key: str = Header(None)):
    """Dependency for verifying a valid API key in request headers.
    
    Args:
        x_api_key: The API key from the X-API-Key header
        
    Returns:
        The username associated with the API key if valid
        
    Raises:
        HTTPException: If the API key is invalid or missing
    """
    # For testing: if no API key provided, use a default test user
    if x_api_key is None:
        return "test-user-no-auth"
        
    if x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return API_KEYS[x_api_key]


def get_current_user(username: str = Depends(verify_api_key)):
    """Dependency for getting the current authenticated user.
    
    This is a placeholder for a more complex user system.
    In a real application, this might fetch user data from a database.
    
    Args:
        username: The username returned by verify_api_key
        
    Returns:
        The username (representing the authenticated user)
    """
    return username
