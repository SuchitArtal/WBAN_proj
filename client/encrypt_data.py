import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import json

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

if __name__ == "__main__":SELECT * FROM users;
    # Get session key from user
    session_key_hex = input("Enter your session key (from authentication): ")
    user_id = input("Enter your user_id: ")
    
    # Example data to encrypt
    data = {
        "heart_rate": 75,
        "blood_pressure": {
            "systolic": 120,
            "diastolic": 80
        },
        "temperature": 36.8,
        "timestamp": 1234567890
    }
    
    # Convert data to JSON string
    plaintext = json.dumps(data)
    
    # Convert session key from hex to bytes
    session_key = bytes.fromhex(session_key_hex)
    
    # Encrypt the data
    encrypted_payload = encrypt_data(session_key, plaintext)
    
    # Create the complete request payload
    request_payload = {
        "user_id": user_id,
        "encrypted_data": encrypted_payload["encrypted_data"],
        "tag": encrypted_payload["tag"],
        "nonce": encrypted_payload["nonce"],
        "session_key": session_key_hex
    }
    
    print("\nUse this payload in your curl command:")
    print(json.dumps(request_payload, indent=2))
    
    print("\nCurl command:")
    print(f"""curl -X POST http://localhost:5000/data \\
-H "Content-Type: application/json" \\
-d '{json.dumps(request_payload)}'""")
