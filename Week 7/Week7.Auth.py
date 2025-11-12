import bcrypt
import os

#Step6: Define the User Data File
USER_DATA_FILE = "users.txt"

#Step4: Implement the Password Hashing Function
def hash_password(plain_text_password):
    #Encode the password to bytes

    password_bytes = plain_text_password.encode('utf-8')
    #Generate a salt
    salt = bcrypt.gensalt()
    #Hash the password 
    hashed = bcrypt.hashpw(password_bytes, salt)

    #Decode the hash back to string
    return hashed.decode('utf-8')

#Step5: Implement the Password Verification Function
def verify_password(plain_text_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False
    
#Step8: Implement User Existence Check
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open (USER_DATA_FILE, 'r') as f:
        for line in f:
            stored_username, _ = line.strip().split(',', 1)
            if stored_username == username:
                return True
    return False   
    
#Step7: Implement User Registration Function
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists")
        return False

    hashed = hash_password(password)

    with open (USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed}\n")
        print(f"User '{username}' registered successfully.")
        return True


#Step9: Implement the login function
def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    with open (USER_DATA_FILE, 'r') as f:
        for line in f:
            stored_username, stored_hash = line.strip().split(',', 1)
            if stored_username == username:
                if verify_password(password, stored_hash):
                    print(f"User '{username}' authenticated successfully.")
                    return True
                else:
                    print("Error: Incorrect password.")
                    return False
    print(f"Error: User name '{username}' not found.")
    return False

#Step10: Input Validation Function
def validate_username(username):
    if not (3 <= len(username) <= 25) or not username.isalnum():
        return False, "Username must be 3-25 characters long and contain only alphanumeric characters."
    return True, ""

def validate_password(password):
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

        

            #Confirm password
            confirm_password = input("Confirm your password: ").strip()
            if password != confirm_password:
                print("Error: Passwords do not match.")
                continue

    

            #Register the username
            register_user(username, password)

        elif choice == '2':
            #Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            login_user(username, password)

        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("\nInvalid option. Please try again. Select 1, 2, or 3.")
if __name__ == "__main__":
    main()           
#

