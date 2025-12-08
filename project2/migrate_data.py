import shutil
from pathlib import Path
import sys

def migrate_from_old_structure():
    old_db_path = Path("DATA/intelligence.db")
    new_db_path = Path("database/platform.db")
    
    if not old_db_path.exists():
        print("Old database not found.")
        return False
    
    new_db_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(old_db_path, new_db_path)
    print(f"Copied database to {new_db_path}")
    return True

if __name__ == "__main__":
    success = migrate_from_old_structure()
    sys.exit(0 if success else 1)