# app/data/schema.py

def create_users_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
    """)

def create_incidents_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT,
            reported_by TEXT
        );
    """)

def create_datasets_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            created_at TEXT NOT NULL,
            size INTEGER
        );
    """)

def create_tickets_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            assigned_to TEXT
        );
    """)


def create_all_tables(conn):
    """
    Creates ALL database tables needed for the platform.
    main.py depends on this function!
    """
    cursor = conn.cursor()
    create_users_table(cursor)
    create_incidents_table(cursor)
    create_datasets_table(cursor)
    create_tickets_table(cursor)
    conn.commit()
