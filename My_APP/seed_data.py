from utils.database import connect_database, create_tables, insert_incident, insert_dataset, insert_ticket, add_user
from utils.auth import hash_password

conn = connect_database()
create_tables(conn)

# seed incidents
incidents = [
    ("Phishing attack detected","High","Open","2025-01-10"),
    ("Ransomware attempt","Critical","Closed","2025-02-05"),
    ("Unauthorized login attempt","Medium","Open","2025-02-18"),
    ("Data breach detected","High","Open","2025-03-01"),
    ("Malware infection detected","Low","Closed","2025-03-07")
]
for t,sv,st,date in incidents:
    insert_incident(conn,t,sv,st,date)

# seed datasets
datasets = [
    ("Cyber Attack Dataset","MITRE ATT&CK","Cybersecurity",1200),
    ("User Behaviour Logs","Internal Systems","Analytics",450),
    ("Threat Intelligence Feeds","OpenCTI","Threat Intel",980),
    ("Network Traffic Samples","Zeek","Cybersecurity",3000),
    ("Authentication Logs","Internal Systems","Logs",860),
]
for name,source,cat,size in datasets:
    insert_dataset(conn,name,source,cat,size)

# seed tickets
tickets = [
    ("Laptop won’t start","High","Open","2025-03-01"),
    ("VPN not connecting","Medium","Closed","2025-02-20"),
    ("Email not syncing","Low","Open","2025-02-28"),
    ("Printer not printing","Low","Open","2025-03-03"),
    ("Password reset request","Medium","Closed","2025-03-05"),
]
for title,priority,status,date in tickets:
    insert_ticket(conn,title,priority,status,date)

# create admin user (username=admin, password=admin123)
admin_pw = hash_password("admin123")
try:
    add_user(conn, "admin", admin_pw, role="admin")
    print("Admin user created: username=admin password=admin123")
except Exception:
    print("Admin user already exists or error creating user.")

print("Seeding complete.")
conn.close()
