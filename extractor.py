"""Batch table extraction from legacy core sources to S3 landing (phase 1 migration)."""

from typing import Any, Dict, List

import pandas as pd


class FullExtractor:
    """Extract complete table data from source"""

    def __init__(self, connector: Any, batch_size: int = 10000):
        self.connector = connector
        self.batch_size = batch_size

    def extract_table(self, table: str) -> pd.DataFrame:
        """Extract complete table"""
        return self.connector.read_table(table)

    def extract_tables_batch(self, tables: List[str]) -> Dict[str, pd.DataFrame]:
        """Extract multiple tables"""
        result = {}
        for table in tables:
            result[table] = self.extract_table(table)
        return result

    def get_row_count(self, table: str) -> int:
        """Get total row count"""
        result = self.connector.execute_query(f"SELECT COUNT(*) as cnt FROM {table}")
        return result[0]["cnt"] if result else 0

    def extract_with_validation(self, table: str) -> Dict[str, Any]:
        """Extract table with metadata"""
        data = self.extract_table(table)
        row_count = self.get_row_count(table)

        return {
            "table": table,
            "data": data,
            "row_count": row_count,
            "columns": list(data.columns),
            "memory_usage_mb": data.memory_usage(deep=True).sum() / 1024 / 1024,
        }
