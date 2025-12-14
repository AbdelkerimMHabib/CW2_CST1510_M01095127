"""Database setup script"""

"""Here, I initialize the database for my platform. It creates all tables and seeds the data where tables are empty"""
from services.database_manager import DatabaseManager
from services.auth_manager import Hasher

def setup_database():
    """Create database tables and seed initial data."""
    #Path to the database folder
    db = DatabaseManager(db_path="DATA/intelligence.db")
    
    # Create tables
    try:
        #User table
        db.execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        #Cybersecurity incidents table
        db.execute_query("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            severity TEXT,
            status TEXT,
            date TEXT
        )
        """)
        
        #Datasets metadata table
        db.execute_query("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            source TEXT,
            category TEXT,
            size INTEGER
        )
        """)
        
        #IT tickets table
        db.execute_query("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            priority TEXT,
            status TEXT,
            created_date TEXT
        )
        """)
        
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        return
    
    #Verify if tables exist and if they contain any data
    try:
        users_count = db.fetch_one("SELECT COUNT(*) as count FROM users")
        incidents_count = db.fetch_one("SELECT COUNT(*) as count FROM cyber_incidents")
        
        # Only seed if tables are empty
        if users_count and users_count["count"] == 0 and incidents_count and incidents_count["count"] == 0:
            # Seed sample data
            seed_sample_data(db)
            print(" Sample data seeded successfully!")
        else:
            print("Database already contains data. No seeding performed.")
    
    except Exception as e:
        print(f"Error checking existing data: {e}")
        return
    
    #Close the database connection
    db.close()
    print(f"Database setup completed at: {db._db_path}")

def seed_sample_data(db):
    """Seed sample data into the database."""
    #cyber incidents
    incidents = [
        ("Phishing attack detected", "High", "open", "2025-01-10"),
        ("Ransomware attempt", "Critical", "closed", "2025-02-05"),
        ("Unauthorized login attempt", "Medium", "open", "2025-02-18"),
        ("Data breach detected", "High", "open", "2025-03-01"),
        ("Malware infection detected", "Low", "closed", "2025-03-07"),
    ]
    
    #insert each Incident
    for incident in incidents:
        db.execute_query(
            "INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)",
            incident
        )
    
    #Datasets
    datasets = [
        ("Cyber Attack Dataset", "MITRE ATT&CK", "Cybersecurity", 1200),
        ("User Behaviour Logs", "Internal Systems", "Analytics", 450),
        ("Threat Intelligence Feeds", "OpenCTI", "Threat Intel", 980),
        ("Network Traffic Samples", "Zeek", "Cybersecurity", 3000),
        ("Authentication Logs", "Internal Systems", "Logs", 860),
    ]
    
    for dataset in datasets:
        db.execute_query(
            "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
            dataset
        )
    
    #IT tickets
    tickets = [
        ("Laptop won't start", "High", "open", "2025-03-01"),
        ("VPN not connecting", "Medium", "closed", "2025-02-20"),
        ("Email not syncing", "Low", "open", "2025-02-28"),
        ("Printer not printing", "Low", "open", "2025-03-03"),
        ("Password reset request", "Medium", "closed", "2025-03-05"),
    ]
    
    for ticket in tickets:
        db.execute_query(
            "INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
            ticket
        )
    
    #Set up admin credentials
    admin_username = "admin"
    admin_password = "admin123"

    #Hash admin password
    hashed = Hasher.hash_password(admin_password)
    
    try:
        db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (admin_username, hashed, "admin")
        )
        print(f"Admin user created: {admin_username}/{admin_password}")
    except Exception as e:
        print(f"Could not create admin user: {e}")

if __name__ == "__main__":
   setup_database()

    