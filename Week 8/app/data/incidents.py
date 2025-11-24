# app/data/incidents.py
import pandas as pd
from .db import connect_db

def insert_incident(title, date, severity, status, description, reported_by):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cyber_incidents (title, date, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, date, severity, status, description, reported_by))

    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df

def update_incident_status(incident_id, new_status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status=? WHERE id=?", (new_status, incident_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated

def delete_incident(incident_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id=?", (incident_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted
