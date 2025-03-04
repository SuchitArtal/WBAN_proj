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
session_key = bytes.fromhex("1357f4fd7660b3f7ec187f0d6b5b3b231733f9a4729e4d34b1bd4af1a1517b06")  # Replace with session key
plaintext = "Heart rate: 75 bpm"
encrypted_payload = encrypt_data(session_key, plaintext)
print(encrypted_payload)
