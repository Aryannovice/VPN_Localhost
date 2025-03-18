import socket
import ssl
import requests
from config import SERVER_HOST, SERVER_PORT, PROXY_URL
from vpn_server.utils import encrypt_data, decrypt_data  # Import encryption functions


def forward_to_proxy(data):
    """Forward encrypted data to the proxy server."""
    try:
        print(f"Forwarding encrypted data to proxy: {data}")
        response = requests.post(PROXY_URL, data=data)  # Send POST request with encrypted data
        print(f"Response from proxy: {response.content}")
        return response.content  # Return encrypted response from proxy
    except Exception as e:
        print(f"Error forwarding data to proxy: {e}")
        return encrypt_data("Error: Unable to process request via proxy.")


def start_vpn_server():
    print("Starting VPN Server...")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="ssl/server.crt", keyfile="ssl/server.key")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print(f"VPN Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        secure_socket = context.wrap_socket(client_socket, server_side=True)

        try:
            # Receive and decrypt incoming request from client
            encrypted_request = secure_socket.recv(8192)  # Use a larger buffer size
            request = decrypt_data(encrypted_request)
            print(f"Received from client: {request}")

            # Forward encrypted request to proxy server and get encrypted response
            encrypted_response_from_proxy = forward_to_proxy(encrypt_data(request))

            if not isinstance(encrypted_response_from_proxy, bytes):
                print("Proxy returned invalid response.")
                secure_socket.send(encrypt_data("Error: Invalid response from proxy."))
                continue

            # Send encrypted response back to client
            secure_socket.send(encrypted_response_from_proxy)
            print("Encrypted response sent back to client.")
        except Exception as e:
            print(f"Error handling client connection: {e}")
        finally:
            secure_socket.close()
            print("Connection closed.")


if __name__ == "__main__":
    start_vpn_server()
