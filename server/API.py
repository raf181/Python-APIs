from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt

# Create a Flask app
app = Flask(__name__)
auth = HTTPBasicAuth()

# Define the path to the log file
log_file_path = 'api_log.log'
# Create a dictionary of users and their hashed passwords
users = {}

# Function to load user data, including password hashes, from a file
def load_user_data():
    # Load user data from 'user_data.txt' into the 'users' dictionary
    with open('user_data.txt', 'r') as file:
        for line in file:
            username, hashed_password = line.strip().split(',')
            users[username] = hashed_password

# Load user data at startup
load_user_data()

# Authentication callback
@auth.verify_password
def verify_password(username, password):
    # Verify user credentials during authentication
    if username in users:
        stored_hash = users[username]
        if sha256_crypt.verify(password, stored_hash):
            return username
        else:
            # Log failed login attempt with timestamp, username, and status
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"Timestamp: {timestamp}, User: {username}, Status: Failed Login Attempt\n")
    return None

# Function to load code from file based on user and key
def load_code_from_file(user, key):
    # Load code and max uses from files based on user and key
    subdirectory = os.path.join('keys', user)
    code_file = os.path.join(subdirectory, f'{key}.py')
    max_uses_file = os.path.join(subdirectory, f'{key}.txt')

    if not os.path.isfile(code_file) or not os.path.isfile(max_uses_file):
        return None, 0

    with open(code_file, 'r') as code_file:
        code = code_file.read()

    with open(max_uses_file, 'r') as max_uses_file:
        max_uses_str = max_uses_file.read()
        try:
            max_uses = int(max_uses_str)
        except ValueError:
            max_uses = 0  # Set to 0 if not a valid integer

    return code, max_uses

# New route for the admin dashboard
@app.route('/admin_dashboard', methods=['GET'])
@auth.login_required
def admin_dashboard():
    if auth.current_user() == 'admin':
        # Read log file to get information for the admin dashboard
        with open(log_file_path, 'r') as log_file:
            log_data = log_file.readlines()

        attempts_data = []
        for entry in log_data:
            entry_data = entry.strip().split(', ')
            timestamp = entry_data[0].split(': ')[1]
            user = entry_data[1].split(': ')[1]
            status = entry_data[2].split(': ')[1]
            key_requested = entry_data[3].split(': ')[1] if len(entry_data) > 3 else ""
            ip_address = entry_data[-1].split(': ')[1] if len(entry_data) > 4 else ""

            attempts_data.append({
                'timestamp': timestamp,
                'user': user,
                'status': status,
                'key_requested': key_requested,
                'ip_address': ip_address
            })

        return render_template('admin_dashboard.html', attempts_data=attempts_data)
    else:
        return jsonify({'error': 'Unauthorized'}), 401

# Route for retrieving code
@app.route('/get_code', methods=['POST'])
@auth.login_required
def get_code():
    user = auth.current_user()
    key = request.json.get('key')

    code, max_uses = load_code_from_file(user, key)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if code is None:
        # Log user data for denied request (key not found)
        user_data = f"Date: {timestamp}, User: {user}, Key Requested: {key}, Status: Denied (Key Not Found)\n"
        with open(log_file_path, 'a') as log_file:
            log_file.write(user_data)

        return jsonify({'error': 'Key not found'}), 404

    elif max_uses > 0:
        max_uses -= 1
        with open(os.path.join('keys', user, f'{key}.txt'), 'w') as max_uses_file:
            max_uses_file.write(str(max_uses))

        # Log user data for successful request
        user_data = f"Timestamp: {timestamp}, User: {user}, Key Requested: {key}, Status: Accepted\n"
        with open(log_file_path, 'a') as log_file:
            log_file.write(user_data)

        return jsonify({'code': code})

    else:
        # Log user data for denied request (exceeded maximum uses)
        user_data = f"Timestamp: {timestamp}, User: {user}, Key Requested: {key}, Status: Denied (Exceeded Maximum Uses)\n"
        with open(log_file_path, 'a') as log_file:
            log_file.write(user_data)

        return jsonify({'error': 'Key has exceeded the maximum number of uses'}), 400

if __name__ == '__main__':
    # ==== HTTP ==== #
    app.run(host='192.168.0.37', port=5000)
    # Run the Flask app in debug mode
    # app.run(debug=True)
    # =============== #

    # ==== HTTPS ==== #
    # Configure SSL/TLS
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('your_certificate.pem', 'your_private_key.pem')
    # Start the Flask app with SSL/TLS
    # app.run(debug=True, host='0.0.0.0', port=443, ssl_context=context)
    # =============== #