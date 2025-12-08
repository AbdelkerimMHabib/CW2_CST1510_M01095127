from database.db import DatabaseInitializer

if __name__ == "__main__":
    print("Setting up database...")
    DatabaseInitializer().initialize()
    print("Database setup complete!")