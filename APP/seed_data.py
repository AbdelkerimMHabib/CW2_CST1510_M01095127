from utils.database import connect_database, create_tables, insert_incident, insert_dataset, insert_ticket, add_user, log_activity
from utils.auth import hash_password
from datetime import datetime, timedelta
import sqlite3

def seed_data():
    conn = connect_database()
    
    print("Seeding database...")
    
    # Drop all tables and recreate
    cursor = conn.cursor()
    
    # Drop tables in correct order (considering foreign keys if any)
    tables = ["ai_analyses", "ai_chat_history", "activity_log", "cyber_incidents", "datasets_metadata", "it_tickets", "users"]
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"Dropped table: {table}")
        except:
            pass
    
    # Recreate all tables
    create_tables(conn)
    print("Created all tables")
    
    # Seed incidents
    incidents = [
        ("Phishing attack detected", "High", "Open", (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"), "Phishing email targeting finance department", "admin"),
        ("Ransomware attempt", "Critical", "Closed", (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"), "Ransomware detected and contained", "admin"),
        ("Unauthorized login attempt", "Medium", "Open", (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"), "Multiple failed login attempts from unknown IP", "admin"),
        ("Data breach detected", "High", "In Progress", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), "Suspected data exfiltration detected", "admin"),
        ("Malware infection detected", "Low", "Resolved", (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"), "Malware cleaned from workstation", "admin"),
        ("DDoS attack", "Critical", "Open", (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), "Distributed Denial of Service attack ongoing", "admin"),
        ("Insider threat detected", "High", "In Progress", (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"), "Suspicious user activity detected", "admin"),
        ("Vulnerability scan completed", "Medium", "Closed", datetime.now().strftime("%Y-%m-%d"), "Quarterly vulnerability scan completed", "admin"),
    ]
    
    for t, sv, st, date, desc, created_by in incidents:
        insert_incident(conn, t, sv, st, date, desc, created_by)
    print(f"Added {len(incidents)} incidents")
    
    # Seed datasets
    datasets = [
        ("Cyber Attack Dataset", "MITRE ATT&CK", "Cybersecurity", 1200, "CSV", "admin"),
        ("User Behaviour Logs", "Internal Systems", "Analytics", 450, "JSON", "admin"),
        ("Threat Intelligence Feeds", "OpenCTI", "Threat Intel", 980, "STIX/TAXII", "admin"),
        ("Network Traffic Samples", "Zeek", "Network", 3000, "PCAP", "admin"),
        ("Authentication Logs", "Internal Systems", "Logs", 860, "JSON", "admin"),
        ("Firewall Logs", "Fortinet", "Logs", 1200, "CSV", "admin"),
        ("Endpoint Detection Data", "CrowdStrike", "Cybersecurity", 1500, "JSON", "admin"),
        ("SIEM Alerts", "Splunk", "Analytics", 2000, "JSON", "admin"),
    ]
    
    for name, source, cat, size, format_type, created_by in datasets:
        insert_dataset(conn, name, source, cat, size, format_type, created_by)
    print(f"Added {len(datasets)} datasets")
    
    # Seed tickets - UPDATED: removed created_by parameter since your table doesn't have it
    tickets = [
        ("Laptop won't start", "High", "Open", (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), "John Doe", "User reports laptop not powering on", ""),
        ("VPN not connecting", "Medium", "Closed", (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"), "IT Support", "VPN connection issues resolved", "Updated VPN client"),
        ("Email not syncing", "Low", "Open", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), "", "Outlook not syncing emails", ""),
        ("Printer not printing", "Low", "Open", datetime.now().strftime("%Y-%m-%d"), "IT Support", "Network printer offline", ""),
        ("Password reset request", "Medium", "Closed", (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"), "", "Password reset completed", "User can now login"),
        ("Software installation", "Medium", "In Progress", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), "Jane Smith", "Adobe Creative Suite installation", ""),
        ("Network connectivity issues", "High", "Open", datetime.now().strftime("%Y-%m-%d"), "Network Team", "Intermittent network drops in Building A", ""),
        ("Monitor replacement", "Low", "Resolved", (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"), "IT Support", "Faulty monitor replaced", "New monitor installed"),
    ]
    
    for title, priority, status, date, assigned_to, desc, resolution in tickets:
        insert_ticket(conn, title, priority, status, date, assigned_to, desc, resolution, "admin")
    print(f"Added {len(tickets)} tickets")
    
    # Create admin user
    admin_pw = hash_password("admin123")
    try:
        add_user(conn, "admin", admin_pw, role="admin")
        print("✓ Admin user created: username=admin password=admin123")
    except Exception as e:
        print(f"Admin user already exists or error: {e}")
    
    # Create regular user
    user_pw = hash_password("user123")
    try:
        add_user(conn, "user", user_pw, role="user")
        print("✓ Regular user created: username=user password=user123")
    except Exception as e:
        print(f"User already exists or error: {e}")
    
    # Log some activities
    try:
        log_activity(conn, "admin", "SEED_DATA", "system", None, "Database seeded with initial data")
        log_activity(conn, "system", "APP_START", "system", None, "Application initialized")
    except:
        print("Note: Activity logging might not be set up yet")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Seeding complete!")
    print("\nAvailable login credentials:")
    print("  Admin: username=admin, password=admin123")
    print("  User:  username=user, password=user123")
    print("\nStart the app with: streamlit run Home.py")

if __name__ == "__main__":
    seed_data()