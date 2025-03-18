import socket
import ssl
from config import SERVER_HOST, SERVER_PORT
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from vpn_server.utils import encrypt_data, decrypt_data  # Import encryption functions

def vpn_client():
    print("Starting VPN Client...")

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("ssl/server.crt")

    # Disable hostname verification temporarily (for testing purposes)
    context.check_hostname = False

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to server at {SERVER_HOST}:{SERVER_PORT}...")

    raw_socket.connect((SERVER_HOST, SERVER_PORT))
    secure_socket = context.wrap_socket(raw_socket, server_hostname=SERVER_HOST)

    try:
        # Encrypt request before sending
        request = "Hello, VPN Server!"
        encrypted_request = encrypt_data(request)
        print(f"Encrypted request: {encrypted_request}")  # Debugging log
        secure_socket.send(encrypted_request)
        print("Encrypted request sent to VPN Server.")

        # Receive and decrypt response from server
        encrypted_response = secure_socket.recv(8192)  # Use a larger buffer size to ensure full message is received
        print(f"Encrypted response: {encrypted_response}")  # Debugging log

        response = decrypt_data(encrypted_response)
        print(f"Response from VPN Server: {response}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        secure_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    vpn_client()
