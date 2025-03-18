import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Shared secret key (32 bytes for AES-256)
key = b"thisisaverysecurekey123456789012"

def encrypt_data(data):
    """Encrypt data using AES-256 with a random IV."""
    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Pad the data to ensure it matches the block size
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    # Encrypt the padded data using AES-256 in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Return the IV concatenated with the encrypted data
    return iv + encrypted_data

def decrypt_data(encrypted_message):
    """Decrypt data using AES-256."""
    # Extract the IV from the first 16 bytes of the encrypted message
    iv = encrypted_message[:16]
    encrypted_data = encrypted_message[16:]

    # Decrypt the encrypted data using AES-256 in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding from the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode()
