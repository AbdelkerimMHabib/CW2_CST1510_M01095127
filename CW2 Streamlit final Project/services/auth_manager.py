"""Authentication manager service class"""
from typing import Optional
from models.user import User
from services.database_manager import DatabaseManager
import bcrypt


#Password hashing class
class Hasher:
    """Password hashing utility using bcrypt."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Return bcrypt hash (utf-8 string)."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        """Verify plaintext password against stored bcrypt hash."""
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except Exception:
            return False

#Authentication manager class
class AuthManager:
    """Handles user registration and login."""
    
    def __init__(self, db_manager: DatabaseManager):
        self._db = db_manager
        self._hasher = Hasher()
    

    #Register a new user
    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        """Register a new user."""
        try:
            # Check if username exists
            existing = self._db.get_user(username)
            if existing:
                return False
            
            # Hash password
            password_hash = self._hasher.hash_password(password)
            
            # Add user to database
            self._db.add_user(username, password_hash, role)
            return True
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    #Login
    def login_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user and return User object."""
        try:
            user_data = self._db.get_user(username)
            if user_data is None:
                return None
            
            # Verify password
            if self._hasher.check_password(password, user_data["password_hash"]):
                return User(
                    username=user_data["username"],
                    password_hash=user_data["password_hash"],
                    role=user_data["role"],
                    user_id=user_data["id"],
                    created_at=user_data.get("created_at")
                )
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None
    
    #Admin and utility functions
    def get_all_users(self):
        """Get all registered users."""
        return self._db.get_all_users()
    
    def update_user_role(self, user_id: int, role: str):
        """Update user role."""
        self._db.update_user_role(user_id, role)
    
    def delete_user(self, user_id: int):
        """Delete user."""
        self._db.delete_user(user_id)
    
    def get_user(self, username: str):
        """Get user by username."""
        return self._db.get_user(username)