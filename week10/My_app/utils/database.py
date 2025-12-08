import sqlite3

def connect_database(db_path):
    """Connect to the SQLite database."""
    conn = sqlite3.connect(db_path)
    return conn

def add_user(conn, username, password_hash):
    """Add a new user to the database."""
    with conn:
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))

def get_user(conn, username):
    """Get user details based on username."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def add_data(conn, a, b, c):
    """Add data to table """
    with conn:
        conn.execute("INSERT INTO data (column_a, column_b, column_c) VALUES (?, ?, ?)", (a, b, c))

def get_data(conn):
    """Retrieve data from the data table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    return cursor.fetchall()

def update_data(conn, index, new_value):
    """Update a specific row in data table."""
    with conn:
        conn.execute("UPDATE data SET column_a = ? WHERE id = ?", (new_value, index))

def delete_data(conn, index):
    """Delete a specific row in the data table."""
    with conn:
        conn.execute("DELETE FROM data WHERE id = ?", (index,))
