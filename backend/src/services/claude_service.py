"""Claude Code integration service."""

import json
import logging
from typing import Any, Dict

from src.config import settings
from src.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class ClaudeService:
    """Service for interacting with Claude Code."""

    def __init__(self):
        """Initialize Claude service."""
        # TODO: Initialize Claude Code SDK when available
        pass

    async def analyze_query(
        self, query: str, session_id: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze user query and generate report components."""
        try:
            # Build context for Claude
            claude_context = self._build_context(query, context)

            # TODO: Execute Claude Code SDK
            # For now, return mock data
            logger.info(f"Analyzing query with Claude: {query}")

            # Mock response
            return {
                "components": [
                    {
                        "type": "Summary",
                        "props": {
                            "text": "分析結果のサマリーです。Claude Code SDKの実装後、実際のデータ分析結果が表示されます。",
                            "metrics": {"total": 0, "status": "pending"},
                        },
                    },
                    {
                        "type": "LineChart",
                        "props": {
                            "data": [
                                {"date": "2024-01-01", "value": 100},
                                {"date": "2024-01-02", "value": 120},
                                {"date": "2024-01-03", "value": 110},
                            ],
                            "lines": [
                                {
                                    "dataKey": "value",
                                    "name": "サンプルデータ",
                                    "color": "#8884d8",
                                }
                            ],
                        },
                    },
                ],
                "metadata": {
                    "query_executed": "-- Mock SQL query",
                    "data_range": "2024-01-01 to 2024-01-03",
                    "row_count": 3,
                },
            }

        except Exception as e:
            logger.error(f"Error in Claude analysis: {str(e)}")
            raise

    def _build_context(self, query: str, context: Dict[str, Any]) -> str:
        """Build context string for Claude."""
        return f"""
ユーザーの質問: {query}

まず、必要なテーブルのスキーマをbqコマンドで確認してから、
適切なSQLクエリを構築してください。

追加コンテキスト: {json.dumps(context, ensure_ascii=False)}
"""