import bcrypt
import os
import re
import secrets
import time




#Step6: Define the User Data File
USER_DATA_FILE = "users.txt"

#Other files
LOCKOUT_FILE = "lockout.txt"
SESSIONS_FILE = "sessions.txt"

LOCKOUT_LIMIT= 3 #number of failed attempts
LOCKOUT_DURATION= 5 * 60 #which is 5 minutes

#Step4: Implement the Password Hashing Function
def hash_password(plain_txt_password):
    """Hashed a password using bcrypt with automatic salt generation"""
    #Encode the password to bytes
    password_bytes = plain_txt_password.encode('utf-8')
    #Generate a salt
    salt = bcrypt.gensalt()
    #Hash the password 
    hashed = bcrypt.hashpw(password_bytes, salt)

    #Decode the hash back to string
    return hashed.decode('utf-8')

#Step5: Implement the Password Verification Function 
def verify_password(plain_txt_password, hashed_password):
    """Verify a plaintext password against a stored bcrypt hash"""
    try:
        return bcrypt.checkpw(plain_txt_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False
    
 #Here Implemement challenge 1(optional)

"""Evaluates the password based on factors: Length, commons patters, and upper, lower cases, special characters, and numbers"""
def The_password_strength(password):
    """Checks the strength of a password"""

    if len(password) < 8:
        return "Weak"
    
    score = 0

    if re.search(r"[A-Z]", password):
            score += 1
    if re.search(r"[a-z]", password):
            score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
    if re.search(r"\d", password):
            score += 1       

    #Checks for common patterns
    cmn_patterns = ["12345", "admin", "qwerty", "password"]
    for pattern in cmn_patterns:
        if pattern.lower() in password.lower():
            score -= 2

    if score <=1:
        return "Weak"
    elif score <=3:
            return "Moderate"
    else:
            return "Strong"

#Step8: Implement User Existence Check
"""This checks if a username already exists in the system"""
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    try:
        with open (USER_DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                pts= line.strip().split(',', 2)
                if len(pts) >=1 and pts[0].lower()==username.lower():
                    return True
    except Exception as e:
        return False
    return False
    
#Step7: Implement User Registration Function
"""This functions registers a new user by storing their username and hashed password, role"""
def register_user(username, password, role='user'):
    username= username.lower()
    role= role.strip().lower()
    if role not in ("user", "admin", "analyst"):
        role= 'user'


    if user_exists(username):
        print(f"Error: Username '{username}' already exists")
        return False
    
    strength= The_password_strength(password)
    print(f"Password strength: {strength}")
    if strength == "Weak":
        print("Error: Password is too weak. Please choose a stronger password.")
        return False

    hashed = hash_password(password)
    with open (USER_DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{username},{hashed},{role}\n")

    print(f"User '{username}' registered successfully as '{role}'.")
    return True



#Here, I am implementing the account lockout system

"""This Reads lockout data from the file"""
def lockout_data():
    """Reads lockout data from the file"""
    data= {}

    if not os.path.exists(LOCKOUT_FILE):
        return data
    
    try:
        with open(LOCKOUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:    
                    continue
                pts = line.strip().split(',', 2)
                if len(pts) != 3:
                    continue
                username, attempts, timestamp = pts

                try:
                    data[username] = {'attempts': int(attempts), 'timestamp': float(timestamp)}
                except ValueError:
                    continue
    except Exception as e:
        return {}
    return data


def save_lockout_data(data):
    """Saves the lockout data to the file"""
    with open(LOCKOUT_FILE, 'w', encoding='utf-8') as f:
        for username, info in data.items():
            f.write(f"{username},{info['attempts']},{info['timestamp']}\n")


def failed_login_attempts(username):
    """Handles a failed login attempt for a user"""
    data = lockout_data()
    if username not in data:
        data[username] = {'attempts':1, 'timestamp': time.time()}    
    else:
        data[username]['attempts'] +=1
        data[username]['timestamp'] = time.time()
        if data[username]['attempts'] >= LOCKOUT_LIMIT:
            print(f"Account '{username}' locked due to too many failed login attempts. Please try again later.")    
    save_lockout_data(data)

def reset_login_attempts(username): 
    """Resets the failed login attempts for a user"""
    data = lockout_data()
    if username in data:
        del data[username]
        save_lockout_data(data)

def is_locked(username):
    """Checks if a user account is locked"""
    data= lockout_data()
    if username in data:
        attempts = data[username]['attempts']
        timestamp = data[username]['timestamp']
        if attempts >= LOCKOUT_LIMIT:
           elapsed = time.time() - timestamp
           if elapsed < LOCKOUT_DURATION: #5 minutes
                remaining= int(LOCKOUT_DURATION-elapsed)
                print(f"Account locked. Try again in {remaining} seconds.")
                return True
           else:
                #Lockout period has expired, reset attempts 
                del data[username]
                save_lockout_data(data)
    return False

   

 #Here, I am implementing challenge 4

def create_session(username):
    """Creates a session token for the logged-in user"""
    session_token = secrets.token_hex(16)
    timestamp = time.time()
    print(f"Session created for user '{username}' with token: {session_token}") 
    print(f"Session timestamp: {timestamp}" )
    with open(SESSIONS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{username},{session_token},{timestamp}\n")
    return session_token
         
#Step9: Implement the login function with session and lockout handling
def login_user(username, password):
    """Authenticates a user by verifying their username and password and managing lockouts"""


    username= username.lower()
    #Check if the account is locked
    if is_locked(username):
        return False
    


    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users are registered yet.")
        return False
    
    with open (USER_DATA_FILE, 'r') as f:
        for line in f:
            pts = line.strip().split(',')
            if len(pts) < 3: 
                continue
            store_username, stored_hashed, stored_role = pts[0], pts[1], pts[2]
            if store_username == username:
                if verify_password(password, stored_hashed):
                    reset_login_attempts(username)
                    print(f"User '{username}' logged in successfully as '{stored_role}'.")
                    create_session(username)
                    return True
                else:
                    print("Error: Incorrect password.")
                    failed_login_attempts(username)
                    return False   

    print(f"Error: Username '{username}' not found.")
    return False


#Step10: Input Validation Function

""" Validates username and password inputs"""
def validate_username(username):
    if not (3 <= len(username) <= 25) or not username.isalnum():
        return False, "Username must be 3-25 characters long and contain only alphanumeric characters."
    return True, ""

def validate_password(password):
    """Validates the password based on length requirements"""
    if not (5 <= len(password) <= 50):
        return False, "Password must be 5-50 characters long."
    return True, ""

#Display Menu Function
def display_menu():
    """Displays the main menu options"""
    print("\n"+ "=" *50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM ")
    print("=" *50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("=" *50)

def main():
    """Main program loop"""
    print("Welcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("Please select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            #Check password strength
            strength = The_password_strength(password)
            print(f"Password strength: {strength}")
            
            #Confirm password
            confirm_password = input("Confirm your password: ").strip()
            if password != confirm_password:
                print("Error: Passwords do not match.")
                continue

    
            #Ask for the user's role
            role = input("Enter role (admin/user/analyst): ").strip().lower()
            if role not in ['admin', 'user', 'analyst']:
                print("Error: Invalid role. Defaulting to 'user'.")
                role = 'user' 

            #Register the username
            register_user(username, password, role)

        elif choice == '2':
            #Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            login_user(username, password)

        elif choice == '3':
            print("Exiting the program")
            break

        else:
            print("\nInvalid option. Please try again. Select 1, 2, or 3.")
if __name__ == "__main__":
    main()           
#

