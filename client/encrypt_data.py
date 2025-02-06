import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_data(session_key, plaintext):
    # Generate a random nonce (12 bytes for AES-GCM)
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(session_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
    return {
        "encrypted_data": ciphertext.hex(),
        "tag": encryptor.tag.hex(),
        "nonce": nonce.hex()
    }

# Example usage
session_key = bytes.fromhex("add777d1de8c66b97b92ec307c6a74dc6df7b16f97e67ef89e7048ba8abef820")  # Replace with session key
plaintext = "Heart rate: 75 bpm"
encrypted_payload = encrypt_data(session_key, plaintext)
print(encrypted_payload)
