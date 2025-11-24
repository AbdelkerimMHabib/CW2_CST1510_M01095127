# app/data/db.py
import sqlite3
from pathlib import Path

DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

def connect_db():
    """Return SQLite connection."""
    return sqlite3.connect(str(DB_PATH))

