#database.py
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any

#paths and database initialization
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "DATA"
DB_PATH = DATA_DIR / "intelligence.db"

def connect_database(path: Optional[str] = None) -> sqlite3.Connection:
    """Connect to SQLite database"""
    if path:
        conn = sqlite3.connect(path)
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
    
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

#user functions
def add_user(conn: sqlite3.Connection, username: str, password_hash: str, role: str = "user"):
    """Add a new user to the database"""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"User '{username}' already exists")

def get_user(conn: sqlite3.Connection, username: str):
    """Get user by username"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def get_all_users(conn: sqlite3.Connection):
    """Get all users"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY id DESC")
    return cursor.fetchall()

def update_user_role(conn: sqlite3.Connection, user_id: int, role: str):
    """Update user role"""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    conn.commit()

def delete_user(conn: sqlite3.Connection, user_id: int):
    """Delete user"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

#Incident functions
def get_all_incidents(conn: sqlite3.Connection):
    """Get all cyber incidents"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents ORDER BY id DESC")
    return cursor.fetchall()

def get_incident(conn: sqlite3.Connection, incident_id: int):
    """Get incident by ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
    return cursor.fetchone()

#Insert an Incident
def insert_incident(conn: sqlite3.Connection, title: str, severity: str, status: str, date: str):
    """Insert new incident"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)",
        (title, severity, status, date)
    )
    conn.commit()

#Update an Incident
def update_incident(conn: sqlite3.Connection, incident_id: int, title: str, severity: str, status: str, date: str):
    """Update existing incident"""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET title=?, severity=?, status=?, date=? WHERE id=?",
        (title, severity, status, date, incident_id)
    )
    conn.commit()

#Delete an Incident
def delete_incident(conn: sqlite3.Connection, incident_id: int):
    """Delete incident"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id=?", (incident_id,))
    conn.commit()

#Dataset functions
def get_all_datasets(conn: sqlite3.Connection):
    """Get all datasets"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata ORDER BY id DESC")
    return cursor.fetchall()

def get_dataset(conn: sqlite3.Connection, dataset_id: int):
    """Get dataset by ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata WHERE id = ?", (dataset_id,))
    return cursor.fetchone()

#Insert a Dataset
def insert_dataset(conn: sqlite3.Connection, name: str, source: str, category: str, size: int):
    """Insert new dataset"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
        (name, source, category, size)
    )
    conn.commit()

#Update a Dataset
def update_dataset(conn: sqlite3.Connection, dataset_id: int, name: str, source: str, category: str, size: int):
    """Update existing dataset"""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE datasets_metadata SET name=?, source=?, category=?, size=? WHERE id=?",
        (name, source, category, size, dataset_id)
    )
    conn.commit()

#Delete a Dataset
def delete_dataset(conn: sqlite3.Connection, dataset_id: int):
    """Delete dataset"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id=?", (dataset_id,))
    conn.commit()

#Ticket functions
def get_all_tickets(conn: sqlite3.Connection):
    """Get all IT tickets"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets ORDER BY id DESC")
    return cursor.fetchall()

def get_ticket(conn: sqlite3.Connection, ticket_id: int):
    """Get ticket by ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets WHERE id = ?", (ticket_id,))
    return cursor.fetchone()

#Insert a Ticket
def insert_ticket(conn: sqlite3.Connection, title: str, priority: str, status: str, created_date: str):
    """Insert new ticket"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
        (title, priority, status, created_date)
    )
    conn.commit()

#Update a Ticket
def update_ticket(conn: sqlite3.Connection, ticket_id: int, title: str, priority: str, status: str, created_date: str):
    """Update existing ticket"""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE it_tickets SET title=?, priority=?, status=?, created_date=? WHERE id=?",
        (title, priority, status, created_date, ticket_id)
    )
    conn.commit()

#Delete a Ticket
def delete_ticket(conn: sqlite3.Connection, ticket_id: int):
    """Delete ticket"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE id=?", (ticket_id,))
    conn.commit()

#statistics functions
def get_statistics(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Get statistics for dashboard - returns nested structure"""
    cursor = conn.cursor()
    
    # Incident statistics
    cursor.execute("SELECT COUNT(*) as total FROM cyber_incidents")
    incidents_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) as open FROM cyber_incidents WHERE status IN ('open', 'in progress')")
    incidents_open = cursor.fetchone()[0]
    
    # Dataset statistics
    cursor.execute("SELECT COUNT(*) as total FROM datasets_metadata")
    datasets_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(size) as total_size FROM datasets_metadata")
    result = cursor.fetchone()[0]
    datasets_size = result if result else 0
    
    # Ticket statistics
    cursor.execute("SELECT COUNT(*) as total FROM it_tickets")
    tickets_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) as open FROM it_tickets WHERE status IN ('open', 'in progress')")
    tickets_open = cursor.fetchone()[0]
    
    # User statistics
    cursor.execute("SELECT COUNT(*) as total FROM users")
    users_total = cursor.fetchone()[0]
    
    # Return NESTED structure
    return {
        "incidents": {"total": incidents_total, "open": incidents_open},
        "datasets": {"total": datasets_total, "total_size": datasets_size},
        "tickets": {"total": tickets_total, "open": tickets_open},
        "users": {"total": users_total}
    }