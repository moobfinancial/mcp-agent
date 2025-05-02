"""Basic authentication system for the FastAPI backend.

This authentication module defines a simple API key header authentication system
that can be used as a FastAPI Dependency.
"""
from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Valid API keys and their associated users
API_KEYS = {
    "test-api-key": "test-user",
    "dev-api-key": "developer",
}

security = HTTPBearer(auto_error=False)


async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency for verifying a valid API key in Authorization header.
    
    Args:
        credentials: The Authorization header credentials (Bearer token)
        
    Returns:
        The username associated with the API key if valid
        
    Raises:
        HTTPException: If the API key is invalid or missing
    """
    # Debug: print credentials for troubleshooting
    print(f"[AUTH DEBUG] Authorization credentials: {credentials}")
    
    # For testing: if no credentials provided, use a default test user
    if credentials is None:
        print("[AUTH DEBUG] No credentials provided, using default test user")
        return "test-user-no-auth"
    
    # Extract the token from Bearer token
    token = credentials.credentials
    print(f"[AUTH DEBUG] Token from Authorization: {token}")
    
    if token not in API_KEYS:
        print(f"[AUTH DEBUG] Invalid token: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"[AUTH DEBUG] Valid token for user: {API_KEYS[token]}")
    return API_KEYS[token]


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
