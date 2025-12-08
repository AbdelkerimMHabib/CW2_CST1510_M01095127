import sqlite3
import bcrypt
from pathlib import Path

class DatabaseInitializer:
    def __init__(self, db_path: str = "database/platform.db"):
        self.db_path = Path(db_path)
        self._ensure_directory()
    
    def _ensure_directory(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def create_tables(self, conn: sqlite3.Connection):
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT NOT NULL,
            category TEXT NOT NULL,
            size INTEGER NOT NULL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_date TEXT NOT NULL
        )
        """)
        
        conn.commit()
    
    def seed_sample_data(self, conn: sqlite3.Connection):
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            return
        
        incidents = [
            ("Phishing attack detected", "High", "open", "2025-01-10"),
            ("Ransomware attempt", "Critical", "closed", "2025-02-05"),
            ("Unauthorized login attempt", "Medium", "open", "2025-02-18"),
        ]
        cursor.executemany("INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)", incidents)
        
        datasets = [
            ("Cyber Attack Dataset", "MITRE ATT&CK", "Cybersecurity", 1200),
            ("User Behaviour Logs", "Internal Systems", "Analytics", 450),
            ("Threat Intelligence Feeds", "OpenCTI", "Threat Intel", 980),
        ]
        cursor.executemany("INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)", datasets)
        
        tickets = [
            ("Laptop won't start", "High", "open", "2025-03-01"),
            ("VPN not connecting", "Medium", "closed", "2025-02-20"),
            ("Email not syncing", "Low", "open", "2025-02-28"),
        ]
        cursor.executemany("INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)", tickets)
        
        admin_password = "admin123"
        hashed = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        try:
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", ("admin", hashed, "admin"))
        except sqlite3.IntegrityError:
            pass
        
        conn.commit()
    
    def initialize(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        self.create_tables(conn)
        self.seed_sample_data(conn)
        
        conn.close()