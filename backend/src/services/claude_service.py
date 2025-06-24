"""Claude Code integration service."""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import anyio
from claude_code_sdk import ClaudeCodeOptions, Message, query

from src.config import settings
from src.prompts import SYSTEM_PROMPT
from src.services.claude_auth_service import ClaudeAuthService

logger = logging.getLogger(__name__)


class ClaudeService:
    """Service for interacting with Claude Code."""

    def __init__(self):
        """Initialize Claude service."""
        self.auth_service = ClaudeAuthService()
        self.options = ClaudeCodeOptions(
            system_prompt=SYSTEM_PROMPT,
            max_turns=1,  # Single turn for report generation
            allowed_tools=["bash"],  # Only allow bash for bq commands
            permission_mode="auto",
        )
        
    async def set_auth_tokens(
        self, 
        access_token: str, 
        refresh_token: str, 
        expires_at: int
    ) -> bool:
        """Set authentication tokens for Claude Code."""
        return await self.auth_service.authenticate_with_tokens(
            access_token, refresh_token, expires_at
        )

    async def analyze_query(
        self, query_text: str, session_id: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze user query and generate report components."""
        try:
            # Build context for Claude
            claude_context = self._build_context(query_text, context)

            # Execute Claude Code
            logger.info(f"Analyzing query with Claude: {query_text}")
            
            messages: List[Message] = []
            result_text = ""
            
            async for message in query(
                prompt=claude_context,
                options=self.options
            ):
                messages.append(message)
                if hasattr(message, 'content'):
                    result_text += message.content
            
            # Parse JSON response from Claude
            try:
                # Extract JSON from the response
                result = self._extract_json_from_response(result_text)
                
                # Validate the response structure
                if "components" not in result:
                    raise ValueError("Invalid response: missing 'components' field")
                
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude response: {e}")
                # Return a fallback response
                return self._create_error_response(
                    "JSONのパースに失敗しました。もう一度お試しください。"
                )

        except Exception as e:
            logger.error(f"Error in Claude analysis: {str(e)}")
            raise

    def _build_context(self, query_text: str, context: Dict[str, Any]) -> str:
        """Build context string for Claude."""
        return f"""
ユーザーの質問: {query_text}

まず、必要なテーブルのスキーマをbqコマンドで確認してから、
適切なSQLクエリを構築してください。

追加コンテキスト: {json.dumps(context, ensure_ascii=False)}

必ず指定されたJSON形式でレスポンスを返してください。
"""
    
    def _extract_json_from_response(self, text: str) -> Dict[str, Any]:
        """Extract JSON from Claude's response."""
        # Try to find JSON in the response
        import re
        
        # Look for JSON block
        json_match = re.search(r'```json\s*({.*?})\s*```', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # Try to parse the entire response as JSON
        return json.loads(text)
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "components": [
                {
                    "type": "Summary",
                    "props": {
                        "text": error_message,
                        "metrics": {"status": "error"},
                    },
                },
            ],
            "metadata": {
                "error": True,
                "message": error_message,
            },
        }