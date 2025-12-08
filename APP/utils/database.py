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
    
    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Cyber incidents table
    c.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        severity TEXT,
        status TEXT,
        date TEXT,
        description TEXT,
        created_by TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Datasets table
    c.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source TEXT,
        category TEXT,
        size INTEGER,
        format TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # IT tickets table
    c.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT,
        assigned_to TEXT,
        description TEXT,
        resolution TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # AI Analyses table
    c.execute("""
    CREATE TABLE IF NOT EXISTS ai_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        entity_id INTEGER NOT NULL,
        analysis_type TEXT NOT NULL,
        analysis_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT
    )""")
    
    # AI Chat History table
    c.execute("""
    CREATE TABLE IF NOT EXISTS ai_chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        domain TEXT NOT NULL,
        message_role TEXT NOT NULL,
        message_content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Activity Log table
    c.execute("""
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        action TEXT NOT NULL,
        entity_type TEXT,
        entity_id INTEGER,
        details TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    conn.commit()

# ---------- Users ----------
def add_user(conn, username: str, password_hash: str, role: str = "user"):
    with conn:
        conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                     (username, password_hash, role))
        log_activity(conn, username, "USER_CREATED", "user", None, f"Created user {username}")

def get_user(conn, username: str) -> Optional[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cur.fetchone()

def update_user_password(conn, username: str, new_password_hash: str):
    with conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE username = ?", 
                    (new_password_hash, username))
        log_activity(conn, username, "PASSWORD_CHANGED", "user", None, "Password updated")

def get_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, username, role, created_at FROM users ORDER BY created_at DESC")
    return cur.fetchall()

# ---------- Cyber incidents CRUD ----------
def insert_incident(conn, title: str, severity: str, status: str, date: str, description: str = "", created_by: str = ""):
    with conn:
        conn.execute("""
        INSERT INTO cyber_incidents (title, severity, status, date, description, created_by) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, severity, status, date, description, created_by))
        log_activity(conn, created_by, "INCIDENT_CREATED", "incident", None, f"Created incident: {title}")

def get_all_incidents(conn) -> List[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents ORDER BY date DESC, id DESC")
    return cur.fetchall()

def get_incident(conn, incident_id: int) -> Optional[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents WHERE id=?", (incident_id,))
    return cur.fetchone()

def update_incident(conn, incident_id: int, title: str, severity: str, status: str, date: str, description: str = "", updated_by: str = ""):
    with conn:
        conn.execute("""
        UPDATE cyber_incidents 
        SET title=?, severity=?, status=?, date=?, description=?, updated_at=CURRENT_TIMESTAMP 
        WHERE id=?
        """, (title, severity, status, date, description, incident_id))
        log_activity(conn, updated_by, "INCIDENT_UPDATED", "incident", incident_id, f"Updated incident: {title}")

def delete_incident(conn, incident_id: int, deleted_by: str = ""):
    incident = get_incident(conn, incident_id)
    with conn:
        conn.execute("DELETE FROM cyber_incidents WHERE id=?", (incident_id,))
        if incident:
            log_activity(conn, deleted_by, "INCIDENT_DELETED", "incident", incident_id, f"Deleted incident: {incident[1]}")

def get_incidents_by_severity(conn, severity: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents WHERE severity=? ORDER BY date DESC", (severity,))
    return cur.fetchall()

def get_incidents_by_status(conn, status: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents WHERE status=? ORDER BY date DESC", (status,))
    return cur.fetchall()

# ---------- Datasets CRUD ----------
def insert_dataset(conn, name: str, source: str, category: str, size: int, format: str = "", created_by: str = ""):
    with conn:
        conn.execute("""
        INSERT INTO datasets_metadata (name, source, category, size, format, created_by) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, source, category, size, format, created_by))
        log_activity(conn, created_by, "DATASET_CREATED", "dataset", None, f"Created dataset: {name}")

def get_all_datasets(conn) -> List[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata ORDER BY created_at DESC")
    return cur.fetchall()

def get_dataset(conn, dataset_id: int) -> Optional[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata WHERE id=?", (dataset_id,))
    return cur.fetchone()

def update_dataset(conn, dataset_id: int, name: str, source: str, category: str, size: int, format: str = "", updated_by: str = ""):
    with conn:
        conn.execute("""
        UPDATE datasets_metadata 
        SET name=?, source=?, category=?, size=?, format=?, created_at=created_at 
        WHERE id=?
        """, (name, source, category, size, format, dataset_id))
        log_activity(conn, updated_by, "DATASET_UPDATED", "dataset", dataset_id, f"Updated dataset: {name}")

def delete_dataset(conn, dataset_id: int, deleted_by: str = ""):
    dataset = get_dataset(conn, dataset_id)
    with conn:
        conn.execute("DELETE FROM datasets_metadata WHERE id=?", (dataset_id,))
        if dataset:
            log_activity(conn, deleted_by, "DATASET_DELETED", "dataset", dataset_id, f"Deleted dataset: {dataset[1]}")

def get_datasets_by_category(conn, category: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata WHERE category=? ORDER BY created_at DESC", (category,))
    return cur.fetchall()

# ---------- IT Tickets CRUD ----------
def insert_ticket(conn, title: str, priority: str, status: str, created_date: str, assigned_to: str = "", description: str = "", resolution: str = "", created_by: str = ""):
    with conn:
        conn.execute("""
        INSERT INTO it_tickets (title, priority, status, created_date, assigned_to, description, resolution, created_by) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, priority, status, created_date, assigned_to, description, resolution, created_by))
        log_activity(conn, created_by, "TICKET_CREATED", "ticket", None, f"Created ticket: {title}")

def get_all_tickets(conn) -> List[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets ORDER BY created_date DESC, id DESC")
    return cur.fetchall()

def get_ticket(conn, ticket_id: int) -> Optional[Tuple]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets WHERE id=?", (ticket_id,))
    return cur.fetchone()

def update_ticket(conn, ticket_id: int, title: str, priority: str, status: str, created_date: str, assigned_to: str = "", description: str = "", resolution: str = "", updated_by: str = ""):
    with conn:
        conn.execute("""
        UPDATE it_tickets 
        SET title=?, priority=?, status=?, created_date=?, assigned_to=?, description=?, resolution=?, updated_at=CURRENT_TIMESTAMP 
        WHERE id=?
        """, (title, priority, status, created_date, assigned_to, description, resolution, ticket_id))
        log_activity(conn, updated_by, "TICKET_UPDATED", "ticket", ticket_id, f"Updated ticket: {title}")

def delete_ticket(conn, ticket_id: int, deleted_by: str = ""):
    ticket = get_ticket(conn, ticket_id)
    with conn:
        conn.execute("DELETE FROM it_tickets WHERE id=?", (ticket_id,))
        if ticket:
            log_activity(conn, deleted_by, "TICKET_DELETED", "ticket", ticket_id, f"Deleted ticket: {ticket[1]}")

def get_tickets_by_priority(conn, priority: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets WHERE priority=? ORDER BY created_date DESC", (priority,))
    return cur.fetchall()

def get_tickets_by_status(conn, status: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets WHERE status=? ORDER BY created_date DESC", (status,))
    return cur.fetchall()

# ---------- AI Functions ----------
def save_ai_analysis(conn, entity_type: str, entity_id: int, analysis_type: str, analysis_text: str, created_by: str):
    """Save AI analysis to database"""
    with conn:
        conn.execute("""
        INSERT INTO ai_analyses (entity_type, entity_id, analysis_type, analysis_text, created_by)
        VALUES (?, ?, ?, ?, ?)
        """, (entity_type, entity_id, analysis_type, analysis_text, created_by))
        log_activity(conn, created_by, "AI_ANALYSIS_SAVED", entity_type, entity_id, f"Saved {analysis_type} analysis")

def get_ai_analyses(conn, entity_type=None, entity_id=None):
    """Get AI analyses from database"""
    cur = conn.cursor()
    
    if entity_type and entity_id:
        cur.execute("""
        SELECT * FROM ai_analyses 
        WHERE entity_type = ? AND entity_id = ?
        ORDER BY created_at DESC
        """, (entity_type, entity_id))
    elif entity_type:
        cur.execute("""
        SELECT * FROM ai_analyses 
        WHERE entity_type = ?
        ORDER BY created_at DESC
        """, (entity_type,))
    else:
        cur.execute("SELECT * FROM ai_analyses ORDER BY created_at DESC")
    
    return cur.fetchall()

def save_chat_message(conn, username: str, domain: str, role: str, content: str):
    """Save chat message to database"""
    with conn:
        conn.execute("""
        INSERT INTO ai_chat_history (username, domain, message_role, message_content)
        VALUES (?, ?, ?, ?)
        """, (username, domain, role, content))

def get_chat_history(conn, username: str, domain=None, limit=50):
    """Get chat history for a user"""
    cur = conn.cursor()
    
    if domain:
        cur.execute("""
        SELECT * FROM ai_chat_history 
        WHERE username = ? AND domain = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """, (username, domain, limit))
    else:
        cur.execute("""
        SELECT * FROM ai_chat_history 
        WHERE username = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """, (username, limit))
    
    return cur.fetchall()

# ---------- Activity Log ----------
def log_activity(conn, username: str, action: str, entity_type: str = None, entity_id: int = None, details: str = ""):
    """Log user activity"""
    with conn:
        conn.execute("""
        INSERT INTO activity_log (username, action, entity_type, entity_id, details)
        VALUES (?, ?, ?, ?, ?)
        """, (username, action, entity_type, entity_id, details))

def get_recent_activities(conn, limit=20):
    """Get recent activities"""
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM activity_log 
    ORDER BY timestamp DESC 
    LIMIT ?
    """, (limit,))
    return cur.fetchall()

# ---------- Dashboard Stats ----------
def get_dashboard_stats(conn):
    """Get all dashboard statistics in one query"""
    cur = conn.cursor()
    
    # Get counts
    cur.execute("SELECT COUNT(*) FROM cyber_incidents")
    incident_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM cyber_incidents WHERE LOWER(status) = 'open'")
    open_incidents = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM datasets_metadata")
    dataset_count = cur.fetchone()[0]
    
    cur.execute("SELECT SUM(size) FROM datasets_metadata")
    total_size = cur.fetchone()[0] or 0
    
    cur.execute("SELECT COUNT(*) FROM it_tickets")
    ticket_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM it_tickets WHERE LOWER(status) = 'open'")
    open_tickets = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]
    
    # Get recent activities
    cur.execute("SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT 5")
    recent_activities = cur.fetchall()
    
    # Get severity distribution
    cur.execute("SELECT severity, COUNT(*) FROM cyber_incidents GROUP BY severity")
    severity_dist = dict(cur.fetchall())
    
    # Get priority distribution
    cur.execute("SELECT priority, COUNT(*) FROM it_tickets GROUP BY priority")
    priority_dist = dict(cur.fetchall())
    
    return {
        "incidents": incident_count,
        "open_incidents": open_incidents,
        "datasets": dataset_count,
        "total_size_mb": total_size,
        "tickets": ticket_count,
        "open_tickets": open_tickets,
        "users": user_count,
        "recent_activities": recent_activities,
        "severity_distribution": severity_dist,
        "priority_distribution": priority_dist
    }