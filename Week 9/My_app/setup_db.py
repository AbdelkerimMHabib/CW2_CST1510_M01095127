# My_app/setup_db.py
from pathlib import Path
import sqlite3
import bcrypt

DATA_DIR = Path(__file__).resolve().parent / "DATA"
DB_PATH = DATA_DIR / "intelligence.db"

def connect_database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables(conn):
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
        title TEXT,
        severity TEXT,
        status TEXT,
        date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source TEXT,
        category TEXT,
        size INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT
    )
    """)

    conn.commit()

def seed_sample_data(conn):
    cursor = conn.cursor()

  
    incidents = [
        ("Phishing attack detected", "High", "open", "2025-01-10"),
        ("Ransomware attempt", "Critical", "closed", "2025-02-05"),
        ("Unauthorized login attempt", "Medium", "open", "2025-02-18"),
        ("Data breach detected", "High", "open", "2025-03-01"),
        ("Malware infection detected", "Low", "closed", "2025-03-07"),
    ]
    cursor.executemany("INSERT INTO cyber_incidents (title,severity,status,date) VALUES (?,?,?,?)", incidents)

    datasets = [
        ("Cyber Attack Dataset", "MITRE ATT&CK", "Cybersecurity", 1200),
        ("User Behaviour Logs", "Internal Systems", "Analytics", 450),
        ("Threat Intelligence Feeds", "OpenCTI", "Threat Intel", 980),
        ("Network Traffic Samples", "Zeek", "Cybersecurity", 3000),
        ("Authentication Logs", "Internal Systems", "Logs", 860),
    ]
    cursor.executemany("INSERT INTO datasets_metadata (name,source,category,size) VALUES (?,?,?,?)", datasets)

    # Sample IT tickets
    tickets = [
        ("Laptop won’t start", "High", "open", "2025-03-01"),
        ("VPN not connecting", "Medium", "closed", "2025-02-20"),
        ("Email not syncing", "Low", "open", "2025-02-28"),
        ("Printer not printing", "Low", "open", "2025-03-03"),
        ("Password reset request", "Medium", "closed", "2025-03-05"),
    ]
    cursor.executemany("INSERT INTO it_tickets (title,priority,status,created_date) VALUES (?,?,?,?)", tickets)

   
    admin_username = "admin"
    admin_password = "admin123"
    hashed = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)", (admin_username, hashed, "admin"))
    except sqlite3.IntegrityError:
        # user exists
        pass

    conn.commit()

def main():
    conn = connect_database()
    create_tables(conn)
    # Only seed if tables empty 
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM cyber_incidents")
    if cur.fetchone()[0] == 0:
        seed_sample_data(conn)
        print("Sample data inserted.")
    else:
        print("Tables exist and appear to have data. No seeding performed.")
    conn.close()
    print("DB ready at:", DB_PATH)

if __name__ == "__main__":
    main()
