import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple

BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "DATA"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "intelligence.db"

def connect_database():
    """Return sqlite3 connection (rows as tuples)."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ---------- Table creation ----------
def create_tables(conn):
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        severity TEXT,
        status TEXT,
        date TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source TEXT,
        category TEXT,
        size INTEGER
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT
    )""")
    conn.commit()

# ---------- Users ----------
def add_user(conn, username: str, password_hash: str, role: str = "user"):
    with conn:
        conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                     (username, password_hash, role))

def get_user(conn, username: str) -> Optional[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cur.fetchone()

def update_user_password(conn, username: str, new_password_hash: str):
    with conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_password_hash, username))

# ---------- Cyber incidents CRUD ----------
def insert_incident(conn, title: str, severity: str, status: str, date: str):
    with conn:
        conn.execute("INSERT INTO cyber_incidents (title,severity,status,date) VALUES (?,?,?,?)",
                     (title, severity, status, date))

def get_all_incidents(conn) -> List[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents ORDER BY date DESC, id DESC")
    return cur.fetchall()

def get_incident(conn, incident_id: int) -> Optional[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents WHERE id=?", (incident_id,))
    return cur.fetchone()

def update_incident(conn, incident_id: int, title: str, severity: str, status: str, date: str):
    with conn:
        conn.execute("UPDATE cyber_incidents SET title=?, severity=?, status=?, date=? WHERE id=?",
                     (title, severity, status, date, incident_id))

def delete_incident(conn, incident_id: int):
    with conn:
        conn.execute("DELETE FROM cyber_incidents WHERE id=?", (incident_id,))

# ---------- Datasets CRUD ----------
def insert_dataset(conn, name: str, source: str, category: str, size: int):
    with conn:
        conn.execute("INSERT INTO datasets_metadata (name,source,category,size) VALUES (?,?,?,?)",
                     (name, source, category, size))

def get_all_datasets(conn) -> List[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata ORDER BY id DESC")
    return cur.fetchall()

def get_dataset(conn, dataset_id: int) -> Optional[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata WHERE id=?", (dataset_id,))
    return cur.fetchone()

def update_dataset(conn, dataset_id: int, name: str, source: str, category: str, size: int):
    with conn:
        conn.execute("UPDATE datasets_metadata SET name=?, source=?, category=?, size=? WHERE id=?",
                     (name, source, category, size, dataset_id))

def delete_dataset(conn, dataset_id: int):
    with conn:
        conn.execute("DELETE FROM datasets_metadata WHERE id=?", (dataset_id,))

# ---------- IT Tickets CRUD ----------
def insert_ticket(conn, title: str, priority: str, status: str, created_date: str):
    with conn:
        conn.execute("INSERT INTO it_tickets (title,priority,status,created_date) VALUES (?,?,?,?)",
                     (title, priority, status, created_date))

def get_all_tickets(conn) -> List[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets ORDER BY created_date DESC, id DESC")
    return cur.fetchall()

def get_ticket(conn, ticket_id: int) -> Optional[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets WHERE id=?", (ticket_id,))
    return cur.fetchone()

def update_ticket(conn, ticket_id: int, title: str, priority: str, status: str, created_date: str):
    with conn:
        conn.execute("UPDATE it_tickets SET title=?, priority=?, status=?, created_date=? WHERE id=?",
                     (title, priority, status, created_date, ticket_id))

def delete_ticket(conn, ticket_id: int):
    with conn:
        conn.execute("DELETE FROM it_tickets WHERE id=?", (ticket_id,))
