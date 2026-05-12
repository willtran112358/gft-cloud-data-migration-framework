"""Data validation and reconciliation"""

from typing import Any, Dict, List

import pandas as pd


class SchemaValidator:
    """Validate schema compatibility"""

    @staticmethod
    def validate_schema(source_schema: Dict, target_schema: Dict) -> Dict:
        """Compare source and target schemas"""
        source_cols = set(source_schema.keys())
        target_cols = set(target_schema.keys())

        return {
            "missing_in_target": list(source_cols - target_cols),
            "extra_in_target": list(target_cols - source_cols),
            "compatible": source_cols == target_cols,
        }


class DataReconciler:
    """Reconcile data between source and target"""

    def __init__(self, source_connector: Any, target_connector: Any):
        self.source = source_connector
        self.target = target_connector

    def compare_row_counts(self, table: str) -> Dict[str, int]:
        """Compare row counts"""
        source_count = self.source.execute_query(
            f"SELECT COUNT(*) as cnt FROM {table}"
        )[0]["cnt"]
        target_count = self.target.execute_query(
            f"SELECT COUNT(*) as cnt FROM {table}"
        )[0]["cnt"]

        return {
            "source_rows": source_count,
            "target_rows": target_count,
            "difference": source_count - target_count,
            "match": source_count == target_count,
        }

    def find_discrepancies(
        self, table: str, key_column: str, sample_size: int = 1000
    ) -> List[Dict]:
        """Find data mismatches"""
        source_data = self.source.read_table(table).head(sample_size)
        target_data = self.target.read_table(table).head(sample_size)

        # Simple comparison
        mismatches = []
        for idx in source_data.index:
            if idx not in target_data.index:
                mismatches.append({"type": "missing", "row": idx})

        return mismatches
