"""Session management service."""

import json
import logging
from typing import Any, Dict, Optional

import redis.asyncio as redis

from src.config import settings

logger = logging.getLogger(__name__)


class SessionService:
    """Service for managing user sessions."""

    def __init__(self):
        """Initialize session service."""
        self.redis_client = None
        self.session_ttl = 3600  # 1 hour

    async def _get_redis(self) -> redis.Redis:
        """Get Redis client."""
        if not self.redis_client:
            self.redis_client = await redis.from_url(
                settings.redis_url, decode_responses=True
            )
        return self.redis_client

    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data."""
        try:
            client = await self._get_redis()
            data = await client.get(f"session:{session_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Error getting session: {str(e)}")
            return None

    async def save_session(
        self, session_id: str, data: Dict[str, Any]
    ) -> None:
        """Save session data."""
        try:
            client = await self._get_redis()
            await client.setex(
                f"session:{session_id}",
                self.session_ttl,
                json.dumps(data, ensure_ascii=False),
            )
        except Exception as e:
            logger.error(f"Error saving session: {str(e)}")

    async def delete_session(self, session_id: str) -> None:
        """Delete session data."""
        try:
            client = await self._get_redis()
            await client.delete(f"session:{session_id}")
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")