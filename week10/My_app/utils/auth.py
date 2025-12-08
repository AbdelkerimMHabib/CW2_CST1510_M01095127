import bcrypt

def hash_password(plain_txt_password):
    """Hash a password using bcrypt with automatic salt generation"""
    # Encode the password to bytes
    password_bytes = plain_txt_password.encode('utf-8')
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Return the hash as a string
    return hashed.decode('utf-8')

def verify_password(plain_txt_password, hashed_password):
    """Verify a plaintext password against a stored bcrypt hash"""
    try:
        # Use checkpw to compare the plaintext password with the hashed password
        return bcrypt.checkpw(plain_txt_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False
