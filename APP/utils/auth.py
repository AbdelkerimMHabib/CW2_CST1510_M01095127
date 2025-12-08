# utils/auth.py (simpler version without bcrypt)
import hashlib
import secrets

def hash_password(plain_txt_password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)  # Generate a random salt
    salted_password = salt + plain_txt_password
    hash_object = hashlib.sha256(salted_password.encode())
    return f"{salt}${hash_object.hexdigest()}"

def verify_password(plain_txt_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        if '$' not in hashed_password:
            # Legacy support for non-salted hashes
            test_hash = hashlib.sha256(plain_txt_password.encode()).hexdigest()
            return test_hash == hashed_password
        
        salt, stored_hash = hashed_password.split('$')
        salted_password = salt + plain_txt_password
        hash_object = hashlib.sha256(salted_password.encode())
        return hash_object.hexdigest() == stored_hash
    except Exception:
        return False