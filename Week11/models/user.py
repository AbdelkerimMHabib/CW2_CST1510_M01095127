class User:
    """ Represents a user in the Multi-Domain Intelligence Platform. """
    
    def __init__(self, username: str, password_hash: str, role: str):
        self.username = username
        self.password_hash = password_hash
        self.role = role
    
    def get_username(self) -> str:
        """ Returns the username of the user. """
        return self.username
    
    def get_role(self) -> str:
        return self.role  
    
    def verify_password(self, password: str, hasher) -> bool:
        """Check if a plain-text password matches this user's hash."""
        return hasher.check_password(password, self.password_hash)  
    
    def __str__(self) -> str:
        return f"User(username={self.username}, role={self.role})"