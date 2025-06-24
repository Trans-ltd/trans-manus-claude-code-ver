"""Custom authentication service for Claude Code with subscription tokens."""

import json
import logging
import os
from typing import Optional

import httpx

from src.config import settings

logger = logging.getLogger(__name__)


class ClaudeAuthService:
    """Service for managing Claude authentication with custom tokens."""

    def __init__(self):
        """Initialize auth service."""
        self.base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None

    async def authenticate_with_tokens(
        self, access_token: str, refresh_token: str, expires_at: int
    ) -> bool:
        """Authenticate using subscription tokens."""
        try:
            # Store tokens
            self.access_token = access_token
            self.refresh_token = refresh_token
            self.expires_at = expires_at

            # Set as environment variable for Claude Code SDK
            os.environ["ANTHROPIC_AUTH_TOKEN"] = f"Bearer {access_token}"
            
            # Validate token
            return await self._validate_token()

        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False

    async def _validate_token(self) -> bool:
        """Validate the current token."""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                }
                
                # Try a simple API call to validate
                response = await client.get(
                    f"{self.base_url}/v1/models",
                    headers=headers,
                )
                
                return response.status_code == 200

        except Exception as e:
            logger.error(f"Token validation failed: {str(e)}")
            return False

    async def refresh_access_token(self) -> Optional[str]:
        """Refresh the access token using refresh token."""
        try:
            async with httpx.AsyncClient() as client:
                # This is a hypothetical endpoint - actual implementation may vary
                response = await client.post(
                    f"{self.base_url}/auth/refresh",
                    json={"refresh_token": self.refresh_token},
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data["access_token"]
                    self.expires_at = data["expires_at"]
                    
                    # Update environment variable
                    os.environ["ANTHROPIC_AUTH_TOKEN"] = f"Bearer {self.access_token}"
                    
                    return self.access_token
                    
        except Exception as e:
            logger.error(f"Token refresh failed: {str(e)}")
            
        return None

    def is_token_expired(self) -> bool:
        """Check if the current token is expired."""
        if not self.expires_at:
            return True
            
        import time
        return time.time() > self.expires_at

    async def get_valid_token(self) -> Optional[str]:
        """Get a valid access token, refreshing if necessary."""
        if self.is_token_expired():
            await self.refresh_access_token()
            
        return self.access_token