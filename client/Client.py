import requests
import json

# Replace with the URL of your Flask API
api_url = 'http://127.0.0.1:5000/get_code'
# api_url = 'http://192.168.0.37:5000/get_code'
# Define the user's credentials
user = 'user2'  # Replace with the desired username
password = 'password2'  # Replace with the user's password
# Define the key you want to use
key = 'key'  # Replace with the desired key

# Create a JSON payload with the key
payload = {'key': key}

# Send a POST request to the API with authentication
response = requests.post(api_url, json=payload, auth=(user, password))

# Check the response status code
if response.status_code == 200:
    data = json.loads(response.text)
    code = data.get('code')
    if code:
        # ==== debug ==== #
        print(code)
        # == end debug == #
        # === execute === #
        # exec(code)
        # = end execute = #
    else:
        print("API response is missing code.")
elif response.status_code == 401:
    print("Wrong password or user. Please check your password and user.")
elif response.status_code == 404:
    print("Key not found. Please check the key.")
else:
    error_data = json.loads(response.text)
    error_message = error_data.get('error', 'Unknown error')
    print(f"Error: {error_message}")