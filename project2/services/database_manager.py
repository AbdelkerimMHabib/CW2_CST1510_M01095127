import sqlite3
import os
from typing import Any, List, Dict, Optional
from pathlib import Path

class DatabaseManager:
    """Handles SQLite database connections and queries."""
    
    def __init__(self, db_path: str = "database/platform.db"):
        self._db_path = Path(db_path)
        self._connection: Optional[sqlite3.Connection] = None
        self._ensure_db_directory()
    
    def _ensure_db_directory(self) -> None:
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row
        return self._connection
    
    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def execute_query(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor
    
    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[Dict]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def fetch_all(self, sql: str, params: tuple = ()) -> List[Dict]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_table_names(self) -> List[str]:
        rows = self.fetch_all("SELECT name FROM sqlite_master WHERE type='table'")
        return [row['name'] for row in rows]
    
    def get_table_count(self, table_name: str) -> int:
        result = self.fetch_one(f"SELECT COUNT(*) as count FROM {table_name}")
        return result['count'] if result else 0