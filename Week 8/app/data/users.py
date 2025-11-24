# app/data/users.py
import bcrypt
from .db import connect_db

def register_user(username, password, role="user"):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Username already exists."

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hashed, role)
    )

    conn.commit()
    conn.close()
    return True, "User registered."

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "User not found."

    if bcrypt.checkpw(password.encode(), row[0].encode()):
        return True, "Success"
    return False, "Incorrect password."
