import bcrypt
import sqlite3
from typing import Optional, List
from models.user import User
from services.database_manager import DatabaseManager

class PasswordHasher:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def check_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except (ValueError, TypeError):
            return False

class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self._db = db_manager
        self._hasher = PasswordHasher()
    
    def register_user(self, username: str, password: str, role: str = "user") -> tuple[bool, str]:
        try:
            existing = self.get_user_by_username(username)
            if existing:
                return False, "Username already exists"
            
            password_hash = self._hasher.hash_password(password)
            
            self._db.execute_query(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            
            return True, "Registration successful"
            
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def login_user(self, username: str, password: str) -> Optional[User]:
        try:
            row = self._db.fetch_one(
                "SELECT id, username, password_hash, role, created_at FROM users WHERE username = ?",
                (username,)
            )
            
            if not row:
                return None
            
            if self._hasher.check_password(password, row['password_hash']):
                return User(
                    user_id=row['id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    role=row['role'],
                    created_at=row['created_at']
                )
            return None
            
        except Exception:
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        row = self._db.fetch_one(
            "SELECT id, username, password_hash, role, created_at FROM users WHERE username = ?",
            (username,)
        )
        
        if not row:
            return None
        
        return User(
            user_id=row['id'],
            username=row['username'],
            password_hash=row['password_hash'],
            role=row['role'],
            created_at=row['created_at']
        )