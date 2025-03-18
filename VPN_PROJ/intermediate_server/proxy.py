from flask import Flask, request
from config import PROXY_HOST, PROXY_PORT
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from vpn_server.utils import encrypt_data, decrypt_data  # Import encryption functions

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def handle_request():
    if request.method == 'POST':
        try:
            encrypted_request = request.data  # Get encrypted data from VPN server
            print(f"Proxy received encrypted data: {encrypted_request}")

            # Decrypt incoming request
            decrypted_request = decrypt_data(encrypted_request)
            print(f"Proxy decrypted data: {decrypted_request}")

            # Process the request and prepare a response
            response_message = f"Processed by Intermediate Proxy Server: {decrypted_request}"
            encrypted_response = encrypt_data(response_message)
            print(f"Proxy encrypted response: {encrypted_response}")

            return encrypted_response, 200

        except Exception as e:
            print(f"Error processing POST request: {e}")
            return "Error processing request", 500

    elif request.method == 'GET':
        print("Received a GET request.")
        return "This is an intermediate proxy server. Use POST requests.", 200


if __name__ == "__main__":
    print(f"Intermediate Proxy Server running on {PROXY_HOST}:{PROXY_PORT}")
    app.run(host=PROXY_HOST, port=PROXY_PORT)
