# app/data/tickets.py
import pandas as pd
from .db import connect_db

def insert_ticket(title, priority, status, created_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
    """, (title, priority, status, created_date))
    conn.commit()
    conn.close()

def get_all_tickets():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df
