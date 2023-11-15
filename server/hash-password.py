import os
from passlib.hash import sha256_crypt

# Function to hash a password
def hash_password(password):
    # Using sha256_crypt for password hashing
    hashed_password = sha256_crypt.using(rounds=535000).hash(password)
    return hashed_password

# Function to check if a user already exists
def user_exists(username):
    with open('user_data.txt', 'r') as file:
        for line in file:
            existing_username, _ = line.strip().split(',')
            if existing_username == username:
                return True
    return False

# Function to create user directory and files
def create_user_files(username, hashed_password):
    # Create a directory for the user
    user_directory = os.path.join('keys', username)
    os.makedirs(user_directory, exist_ok=True)

    # Create key.txt with content '100'
    with open(os.path.join(user_directory, 'key.txt'), 'w') as key_txt:
        key_txt.write('100')

    # Create key.py with content 'print("Hello world")'
    with open(os.path.join(user_directory, 'key.py'), 'w') as key_py:
        key_py.write('print("Hello world")')

# Get user input for username and password
username = input("Enter username: ")

# Check if the user already exists
if user_exists(username):
    print("User already exists. Password not updated.")
else:
    password = input("Enter password: ")

    # Hash the password
    hashed_password = hash_password(password)

    # Verify the password before storing
    if sha256_crypt.verify(password, hashed_password):
        # Store username and hashed password in a file
        with open('user_data.txt', 'a') as file:
            file.write(f"{username},{hashed_password}\n")
        print("User data stored successfully.")

        # Create user directory and files
        create_user_files(username, hashed_password)
        print(f"User directory and files created for {username}.")
    else:
        print("Password verification failed. User data not stored.")