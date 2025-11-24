# app/data/datasets.py
import pandas as pd
from .db import connect_db

def insert_dataset(name, source, category, size):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata (name, source, category, size)
        VALUES (?, ?, ?, ?)
    """, (name, source, category, size))

    conn.commit()
    conn.close()

def get_all_datasets():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df
