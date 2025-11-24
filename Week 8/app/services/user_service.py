# app/services/user_service.py
from pathlib import Path
from app.data.db import connect_db

DATA_DIR = Path("DATA")

def migrate_users_from_file():
    file_path = DATA_DIR / "users.txt"
    if not file_path.exists():
        return 0

    conn = connect_db()
    cursor = conn.cursor()
    migrated = 0

    with open(file_path, "r") as f:
        f.readline()
        for line in f:
            username, password_hash, role = [x.strip() for x in line.split(",")]
            cursor.execute("""
                INSERT OR IGNORE INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, password_hash, role))
            migrated += cursor.rowcount

    conn.commit()
    conn.close()
    return migrated
