"""BigQuery API endpoints for testing and validation."""

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status

from src.services.bigquery_service import BigQueryService

logger = logging.getLogger(__name__)
router = APIRouter()

bigquery_service = BigQueryService()


@router.get("/validate")
async def validate_connection() -> Dict[str, Any]:
    """Validate BigQuery connection."""
    try:
        is_valid = bigquery_service.validate_connection()
        return {
            "status": "connected" if is_valid else "failed",
            "project_id": bigquery_service.project_id,
            "dataset_id": bigquery_service.dataset_id,
        }
    except Exception as e:
        logger.error(f"Connection validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate BigQuery connection",
        )


@router.get("/tables")
async def list_tables() -> List[str]:
    """List all tables in the dataset."""
    try:
        tables = await bigquery_service.list_tables()
        return tables
    except Exception as e:
        logger.error(f"Failed to list tables: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list tables",
        )


@router.get("/tables/{table_name}/schema")
async def get_table_schema(table_name: str) -> List[Dict[str, Any]]:
    """Get schema for a specific table."""
    try:
        schema = await bigquery_service.get_table_schema(table_name)
        return schema
    except Exception as e:
        logger.error(f"Failed to get table schema: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get table schema",
        )