"""Reports API endpoints."""

import logging
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.services.claude_service import ClaudeService
from src.services.session_service import SessionService

logger = logging.getLogger(__name__)
router = APIRouter()

claude_service = ClaudeService()
session_service = SessionService()


class ReportGenerateRequest(BaseModel):
    """Request model for report generation."""

    query: str = Field(..., description="Natural language query")
    session_id: Optional[str] = Field(None, description="Session ID for context")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class ComponentConfig(BaseModel):
    """Component configuration."""

    type: str = Field(..., description="Component type")
    props: Dict[str, Any] = Field(..., description="Component properties")


class ReportGenerateResponse(BaseModel):
    """Response model for report generation."""

    session_id: str = Field(..., description="Session ID")
    components: List[ComponentConfig] = Field(..., description="UI components")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Response metadata")


@router.post("/generate", response_model=ReportGenerateResponse)
async def generate_report(request: ReportGenerateRequest) -> ReportGenerateResponse:
    """Generate a report based on natural language query."""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Get session context
        session_context = await session_service.get_session(session_id)

        # Execute Claude analysis
        logger.info(f"Processing query: {request.query}")
        result = await claude_service.analyze_query(
            query=request.query,
            session_id=session_id,
            context={
                **(session_context or {}),
                **(request.context or {}),
            },
        )

        # Save session context
        await session_service.save_session(session_id, result.get("metadata", {}))

        return ReportGenerateResponse(
            session_id=session_id,
            components=result["components"],
            metadata=result.get("metadata"),
        )

    except TimeoutError:
        logger.error("Request timed out")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={
                "code": "TIMEOUT",
                "userMessage": "分析に時間がかかりすぎました。クエリを簡略化してお試しください。",
            },
        )
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "CLAUDE_ERROR",
                "userMessage": "分析に失敗しました。もう一度お試しください。",
            },
        )


@router.get("/session/{session_id}")
async def get_session(session_id: str) -> Dict[str, Any]:
    """Get session information."""
    session_data = await session_service.get_session(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return session_data