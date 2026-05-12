"""Base connector abstraction for data sources"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import pandas as pd


class BaseConnector(ABC):
    """Abstract base class for database connectors"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self._connect()

    @abstractmethod
    def _connect(self) -> None:
        """Establish connection to data source"""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> List[Dict]:
        """Execute SQL query and return results"""
        pass

    @abstractmethod
    def get_schema(self, table: str) -> Dict[str, str]:
        """Get table schema (column names and types)"""
        pass

    @abstractmethod
    def read_table(self, table: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Read table data into DataFrame"""
        pass

    @abstractmethod
    def write_table(
        self, table: str, data: pd.DataFrame, mode: str = "append"
    ) -> Dict:
        """Write data to table (append, replace, upsert)"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close connection"""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
