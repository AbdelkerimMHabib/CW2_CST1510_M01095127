class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""
    
    def __init__(self, user_id: int, username: str, password_hash: str, role: str, created_at: str):
        self.__id = user_id
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role
        self.__created_at = created_at
    
    def get_id(self) -> int:
        return self.__id
    
    def get_username(self) -> str:
        return self.__username
    
    def get_role(self) -> str:
        return self.__role
    
    def get_created_at(self) -> str:
        return self.__created_at
    
    def get_password_hash(self) -> str:
        return self.__password_hash
    
    def verify_password(self, plain_password: str, hasher) -> bool:
        """Check if a plain-text password matches this user's hash."""
        return hasher.check_password(plain_password, self.__password_hash)
    
    def is_admin(self) -> bool:
        return self.__role == "admin"
    
    def is_editor(self) -> bool:
        return self.__role in ["admin", "editor"]
    
    def __str__(self) -> str:
        return f"User(id={self.__id}, username={self.__username}, role={self.__role})"