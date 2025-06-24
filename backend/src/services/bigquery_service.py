"""BigQuery integration service."""

import logging
import os
from typing import Any, Dict, List, Optional

from google.cloud import bigquery
from google.oauth2 import service_account

from src.config import settings

logger = logging.getLogger(__name__)


class BigQueryService:
    """Service for interacting with BigQuery."""

    def __init__(self):
        """Initialize BigQuery service."""
        self.client = self._create_client()
        self.project_id = settings.bq_project_id
        self.dataset_id = settings.bq_dataset_id

    def _create_client(self) -> bigquery.Client:
        """Create BigQuery client with service account credentials."""
        try:
            # Create credentials from environment variables
            service_account_info = {
                "type": "service_account",
                "project_id": settings.bq_project_id,
                "private_key_id": settings.bq_private_key_id,
                "private_key": settings.bq_private_key.replace("\\n", "\n"),
                "client_email": settings.bq_client_email,
                "client_id": settings.bq_client_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{settings.bq_client_email}",
            }

            # Create credentials
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=["https://www.googleapis.com/auth/bigquery.readonly"],
            )

            # Create and return client
            return bigquery.Client(
                credentials=credentials,
                project=settings.bq_project_id,
            )

        except Exception as e:
            logger.error(f"Failed to create BigQuery client: {str(e)}")
            raise

    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a BigQuery query and return results."""
        try:
            # Configure query job
            job_config = bigquery.QueryJobConfig(
                use_query_cache=True,
                timeout_ms=settings.bigquery_timeout * 1000,  # Convert to milliseconds
            )

            # Execute query
            query_job = self.client.query(query, job_config=job_config)
            
            # Wait for results
            results = query_job.result(timeout=settings.bigquery_timeout)
            
            # Convert to list of dictionaries
            rows = []
            for row in results:
                rows.append(dict(row))
            
            logger.info(f"Query executed successfully, returned {len(rows)} rows")
            return rows

        except Exception as e:
            logger.error(f"BigQuery query failed: {str(e)}")
            raise

    async def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema for a specific table."""
        try:
            table_ref = f"{self.project_id}.{self.dataset_id}.{table_name}"
            table = self.client.get_table(table_ref)
            
            schema = []
            for field in table.schema:
                schema.append({
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description,
                })
            
            return schema

        except Exception as e:
            logger.error(f"Failed to get table schema: {str(e)}")
            raise

    async def list_tables(self) -> List[str]:
        """List all tables in the dataset."""
        try:
            dataset_ref = f"{self.project_id}.{self.dataset_id}"
            tables = self.client.list_tables(dataset_ref)
            
            table_names = []
            for table in tables:
                table_names.append(table.table_id)
            
            return table_names

        except Exception as e:
            logger.error(f"Failed to list tables: {str(e)}")
            raise

    def validate_connection(self) -> bool:
        """Validate BigQuery connection."""
        try:
            # Try to list datasets as a connection test
            datasets = list(self.client.list_datasets(max_results=1))
            return True
        except Exception as e:
            logger.error(f"BigQuery connection validation failed: {str(e)}")
            return False