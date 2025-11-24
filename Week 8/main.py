
import sqlite3
import pandas as pd
from pathlib import Path
import bcrypt

DB_PATH = Path("DATA/intelligence_platform.db")
DB_PATH.parent.mkdir(exist_ok=True)



def get_connection():
    return sqlite3.connect(DB_PATH)



def create_all_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            incident_type TEXT,
            date TEXT,
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()



def register_user(conn, username, password):
    cursor = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def login_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    row = cursor.fetchone()

    if not row:
        return False
    
    return bcrypt.checkpw(password.encode(), row[0].encode())



def insert_incident(conn, title, incident_type, date, severity, status, description, reported_by):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (title, incident_type, date, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, incident_type, date, severity, status, description, reported_by))

    conn.commit()
    return cursor.lastrowid


def get_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents WHERE id=?", (incident_id,))
    return cursor.fetchone()


def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status=? WHERE id=?",
        (new_status, incident_id)
    )
    conn.commit()


def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id=?", (incident_id,))
    conn.commit()


def incidents_by_severity(conn):
    return pd.read_sql_query("""
        SELECT severity, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY severity
    """, conn)



def main():
    conn = get_connection()
    create_all_tables(conn)

    print("Database ready.\n")

    print("Registering user...")
    uid = register_user(conn, "admin", "password123")
    print("User registered:", uid)

    print("Logging in...")
    print("Login success:", login_user(conn, "admin", "password123"))

    print("\nInserting test incident...")
    iid = insert_incident(
        conn,
        title="Test Incident",
        incident_type="Phishing",
        date="2025-01-01",
        severity="High",
        status="Open",
        description="Testing system",
        reported_by="admin"
    )
    print("Incident ID:", iid)

    print("\nReading incident:")
    print(get_incident(conn, iid))

    print("\nUpdating incident status...")
    update_incident_status(conn, iid, "Closed")
    print(get_incident(conn, iid))

    print("\nDeleting incident...")
    delete_incident(conn, iid)

    print("\nAnalytics:")
    print(incidents_by_severity(conn))


if __name__ == "__main__":
    main()


