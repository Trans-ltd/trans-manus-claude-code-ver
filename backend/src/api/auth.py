"""Authentication API endpoints."""

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.services.claude_service import ClaudeService

logger = logging.getLogger(__name__)
router = APIRouter()

claude_service = ClaudeService()


class AuthTokenRequest(BaseModel):
    """Request model for setting auth tokens."""
    
    access_token: str
    refresh_token: str
    expires_at: int


class AuthTokenResponse(BaseModel):
    """Response model for auth token operations."""
    
    success: bool
    message: str


@router.post("/set-tokens", response_model=AuthTokenResponse)
async def set_auth_tokens(request: AuthTokenRequest) -> AuthTokenResponse:
    """Set authentication tokens for Claude Code."""
    try:
        success = await claude_service.set_auth_tokens(
            access_token=request.access_token,
            refresh_token=request.refresh_token,
            expires_at=request.expires_at
        )
        
        if success:
            return AuthTokenResponse(
                success=True,
                message="認証トークンが正常に設定されました"
            )
        else:
            return AuthTokenResponse(
                success=False,
                message="認証トークンの検証に失敗しました"
            )
            
    except Exception as e:
        logger.error(f"Failed to set auth tokens: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="認証トークンの設定に失敗しました"
        )