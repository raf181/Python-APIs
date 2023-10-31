# API

## Install

Clone the repository: `git clone`
Requirements: `flask`, `flask_httpauth`

```bash
git clone https://github.com/raf181/Python-APIs.git
```

## Configuration

Add users and their passwords

```python
# Define the dictionary of users and their hashed passwords  (these will be more secure in the future).
users = {
    "user1": sha256_crypt.hash("password1"),
    "user2": sha256_crypt.hash("password2"),
}

# Define the path to the log file
log_file_path = 'api_log.log'

```

Add your server IP and port

```python
    app.run(host='YOUR_IP', port=YOUR_PORT)
    # app.run(debug=True) # these is to run it localy on 127.0.0.1
```

This is the file structure that the API requires to work:

The `key.py` contains the code that is sent to the client and the `key.txt` contains the number of times that the key.py can be requested.
The passwords for each user and their password are stored in `API.py`.

```md
└─── server
         ├─── API.py
         ├─── api_log.log
         └─── keys
                ├─── user1
                │     ├─── key.py
                │     ├─── key.txt
                │     ├─── key2.py
                │     └─── key2.txt
                │
                └─── user2
                      ├─── key.py
                      └─── key.txt
```

## API codes

- `200` -  Request was successful.
- `400` - Key has exceeded the maximum number of uses.
- `401` - Wrong password or user.
- `404` - Key not found.

## Security

By default, the server uses HTTP, which makes the client sending the password to the server insecure. To enhance security, you can configure the server to use HTTPS, but you'll need an SSL certificate.

Here's a general outline of how to generate a self-signed SSL certificate using OpenSSL, a commonly used tool for this purpose:

1. **Install OpenSSL**:
   - If you don't already have OpenSSL installed, you can install it on your operating system. The following command can be used on Debian-based systems (e.g., Ubuntu):

      ```bash
      sudo apt-get install openssl
      ```

2. **Generate a Private Key**:
   - Use OpenSSL to generate a 2048-bit RSA private key. You can also add a passphrase to protect the key (optional). The following command generates a private key with a passphrase:

      ```bash
      openssl genpkey -algorithm RSA -aes256 -out server.key
      ```

3. **Generate a Self-Signed Certificate**:
   - Use the private key to create a self-signed certificate. The following command generates a self-signed certificate and specifies a validity period of 365 days:

      ```bash
      openssl req -x509 -key server.key -out server.crt -days 365
      ```

   Keep in mind that self-signed certificates are not trusted by web browsers by default, and users will typically see warnings when accessing a site secured with a self-signed certificate.

Please note that self-signed certificates are primarily for local development and testing environments.

# Client

Configuration:

```python
# Replace with the URL of your Flask API
api_url = 'http://YOUR_IP:PORT/get_code'
user = 'user2'  # Replace with the desired username
password = 'password2'  # Replace with the user's password
# Define the key you want to use
key = 'key'  # Replace with the desired key
```

Keep in mind that these will also have to be set on the file paths and the `APY.py` file.
Also keep in mind that the script is set to debug mode by default, uncoment the `exec(code)` and coment the `print(code)`.

```python
    # ==== debug ==== #
    print(code)
    # == end debug == #
    # === execute === #
    # exec(code)
    # = end execute = #
```

