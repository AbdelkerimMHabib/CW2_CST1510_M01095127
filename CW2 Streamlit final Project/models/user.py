"""User entity class"""
from typing import Optional

class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""
    
    def __init__(self, username: str, password_hash: str, role: str, user_id: Optional[int] = None, created_at: str = None):
        """Initialize User instance."""
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role
        self.__id = user_id
        self.__created_at = created_at
    
    #Getters
    def get_id(self) -> Optional[int]:
        """Returns the user ID"""
        return self.__id
    
    def get_username(self) -> str:
        """Returns the username"""
        return self.__username
    
    def get_role(self) -> str:
        """Returns the user role"""
        return self.__role
    
    def get_password_hash(self) -> str:
        """Returns the password hash"""
        return self.__password_hash
    
    def get_created_at(self) -> Optional[str]:
        """Returns the creation timestamp"""
        return self.__created_at
    
    #utility methods
    def verify_password(self, plain_password: str, hasher) -> bool:
        """Check if a plain-text password matches this user's hash."""
        return hasher.check_password(plain_password, self.__password_hash)
    
    #String representation
    def __str__(self) -> str:
        """Returns string representation of the user"""
        return f"User({self.__username}, role={self.__role})"