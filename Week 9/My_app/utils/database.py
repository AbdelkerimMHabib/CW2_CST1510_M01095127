# My_app/utils/database.py
import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "DATA"
DB_PATH = DATA_DIR / "intelligence.db"

def connect_database(path: Optional[str] = None) -> sqlite3.Connection:
    if path:
        conn = sqlite3.connect(path)
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
    
    conn.row_factory = sqlite3.Row
    return conn

def add_user(conn: sqlite3.Connection, username: str, password_hash: str, role: str = "user"):
    with conn:
        conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))

def get_user(conn: sqlite3.Connection, username: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cur.fetchone()

def verify_user(conn: sqlite3.Connection, username: str, password: str) -> bool:
    user = get_user(conn, username)
    if not user:
        return False
    from utils.auth import verify_password
    return verify_password(password, user["password_hash"])

def get_user_role(conn: sqlite3.Connection, username: str) -> Optional[str]:
    user = get_user(conn, username)
    return user["role"] if user else None


def get_all_incidents(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents ORDER BY id DESC")
    return cur.fetchall()

def get_incident(conn: sqlite3.Connection, incident_id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
    return cur.fetchone()

def insert_incident(conn: sqlite3.Connection, title: str, severity: str, status: str, date: str):
    with conn:
        conn.execute("INSERT INTO cyber_incidents (title,severity,status,date) VALUES (?,?,?,?)", (title, severity, status, date))

def update_incident(conn: sqlite3.Connection, incident_id: int, title: str, severity: str, status: str, date: str):
    with conn:
        conn.execute("UPDATE cyber_incidents SET title=?, severity=?, status=?, date=? WHERE id=?", (title, severity, status, date, incident_id))

def delete_incident(conn: sqlite3.Connection, incident_id: int):
    with conn:
        conn.execute("DELETE FROM cyber_incidents WHERE id=?", (incident_id,))


def get_all_datasets(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata ORDER BY id DESC")
    return cur.fetchall()


def get_all_tickets(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets ORDER BY id DESC")
    return cur.fetchall()
