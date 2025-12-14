"""Database manager service class"""
import sqlite3
from typing import Any, Iterable, List, Dict, Optional
from pathlib import Path

class DatabaseManager:
    """Handles SQLite database connections and queries."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            BASE_DIR = Path(__file__).resolve().parent.parent
            #Directs to my exisitng database folder
            self._db_path = BASE_DIR / "DATA" / "intelligence.db"
        else:
            self._db_path = Path(db_path)
        
        self._connection: Optional[sqlite3.Connection] = None
        self._ensure_database_directory()
    
    def _ensure_database_directory(self):
        """Ensure database directory exists."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self) -> None:
        """Establish database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row
    
    def close(self) -> None:
        """Close database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def execute_query(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Cursor:
        """Execute a write query (INSERT, UPDATE, DELETE)."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        self._connection.commit()
        return cur
    
    def fetch_one(self, sql: str, params: Iterable[Any] = ()) -> Optional[Dict]:
        """Fetch a single row from the database."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        row = cur.fetchone()
        return dict(row) if row else None
    
    def fetch_all(self, sql: str, params: Iterable[Any] = ()) -> List[Dict]:
        """Fetch all rows from the database."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    
    # User operations
    def add_user(self, username: str, password_hash: str, role: str = "user") -> int:
        """Add a new user to the database."""
        cursor = self.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        return cursor.lastrowid
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username."""
        return self.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
    
    def get_all_users(self) -> List[Dict]:
        """Get all users."""
        return self.fetch_all("SELECT id, username, role, created_at FROM users ORDER BY id DESC")
    
    def update_user_role(self, user_id: int, role: str):
        """Update user role."""
        self.execute_query("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    
    def delete_user(self, user_id: int):
        """Delete user."""
        self.execute_query("DELETE FROM users WHERE id = ?", (user_id,))
    
    # Incident operations
    def get_all_incidents(self) -> List[Dict]:
        """Get all cyber incidents."""
        return self.fetch_all("SELECT * FROM cyber_incidents ORDER BY id DESC")
    
    def get_incident(self, incident_id: int) -> Optional[Dict]:
        """Get incident by ID."""
        return self.fetch_one("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
    
    def insert_incident(self, title: str, severity: str, status: str, date: str) -> int:
        """Insert new incident."""
        cursor = self.execute_query(
            "INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)",
            (title, severity, status, date)
        )
        return cursor.lastrowid
    
    def update_incident(self, incident_id: int, title: str, severity: str, status: str, date: str):
        """Update existing incident."""
        self.execute_query(
            "UPDATE cyber_incidents SET title=?, severity=?, status=?, date=? WHERE id=?",
            (title, severity, status, date, incident_id)
        )
    
    def delete_incident(self, incident_id: int):
        """Delete incident."""
        self.execute_query("DELETE FROM cyber_incidents WHERE id=?", (incident_id,))
    
    # Dataset operations
    def get_all_datasets(self) -> List[Dict]:
        """Get all datasets."""
        return self.fetch_all("SELECT * FROM datasets_metadata ORDER BY id DESC")
    
    def get_dataset(self, dataset_id: int) -> Optional[Dict]:
        """Get dataset by ID."""
        return self.fetch_one("SELECT * FROM datasets_metadata WHERE id = ?", (dataset_id,))
    
    def insert_dataset(self, name: str, source: str, category: str, size: int) -> int:
        """Insert new dataset."""
        cursor = self.execute_query(
            "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
            (name, source, category, size)
        )
        return cursor.lastrowid
    
    def update_dataset(self, dataset_id: int, name: str, source: str, category: str, size: int):
        """Update existing dataset."""
        self.execute_query(
            "UPDATE datasets_metadata SET name=?, source=?, category=?, size=? WHERE id=?",
            (name, source, category, size, dataset_id)
        )
    
    def delete_dataset(self, dataset_id: int):
        """Delete dataset."""
        self.execute_query("DELETE FROM datasets_metadata WHERE id=?", (dataset_id,))
    
    # Ticket operations
    def get_all_tickets(self) -> List[Dict]:
        """Get all IT tickets."""
        return self.fetch_all("SELECT * FROM it_tickets ORDER BY id DESC")
    
    def get_ticket(self, ticket_id: int) -> Optional[Dict]:
        """Get ticket by ID."""
        return self.fetch_one("SELECT * FROM it_tickets WHERE id = ?", (ticket_id,))
    
    def insert_ticket(self, title: str, priority: str, status: str, created_date: str) -> int:
        """Insert new ticket."""
        cursor = self.execute_query(
            "INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
            (title, priority, status, created_date)
        )
        return cursor.lastrowid
    
    def update_ticket(self, ticket_id: int, title: str, priority: str, status: str, created_date: str):
        """Update existing ticket."""
        self.execute_query(
            "UPDATE it_tickets SET title=?, priority=?, status=?, created_date=? WHERE id=?",
            (title, priority, status, created_date, ticket_id)
        )
    
    def delete_ticket(self, ticket_id: int):
        """Delete ticket."""
        self.execute_query("DELETE FROM it_tickets WHERE id=?", (ticket_id,))
    
    # Statistics function
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics for dashboard - returns nested structure."""
        stats = {}
        
        # Incident statistics
        incidents_data = self.fetch_one("SELECT COUNT(*) as total FROM cyber_incidents")
        incidents_open = self.fetch_one(
            "SELECT COUNT(*) as open FROM cyber_incidents WHERE status IN ('open', 'in progress')"
        )
        stats["incidents"] = {
            "total": incidents_data["total"] if incidents_data else 0,
            "open": incidents_open["open"] if incidents_open else 0
        }
        
        # Dataset statistics
        datasets_data = self.fetch_one("SELECT COUNT(*) as total FROM datasets_metadata")
        datasets_size = self.fetch_one("SELECT SUM(size) as total_size FROM datasets_metadata")
        stats["datasets"] = {
            "total": datasets_data["total"] if datasets_data else 0,
            "total_size": datasets_size["total_size"] if datasets_size and datasets_size["total_size"] else 0
        }
        
        # Ticket statistics
        tickets_data = self.fetch_one("SELECT COUNT(*) as total FROM it_tickets")
        tickets_open = self.fetch_one(
            "SELECT COUNT(*) as open FROM it_tickets WHERE status IN ('open', 'in progress')"
        )
        stats["tickets"] = {
            "total": tickets_data["total"] if tickets_data else 0,
            "open": tickets_open["open"] if tickets_open else 0
        }
        
        # User statistics
        users_data = self.fetch_one("SELECT COUNT(*) as total FROM users")
        stats["users"] = {"total": users_data["total"] if users_data else 0}
        
        return stats