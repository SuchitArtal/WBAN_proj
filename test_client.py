import requests
import json
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import random

class WBANDeviceSimulator:
    def __init__(self, base_url, user_id, password):
        self.base_url = base_url
        self.user_id = user_id
        self.password = password
        self.session_key = None
        self.pseudo_identity = None
        
    def authenticate(self):
        """Authenticate with the server and get a session key"""
        # Generate pseudo-identity from user_id
        self.pseudo_identity = self._generate_pseudo_identity(self.user_id)
        
        auth_data = {
            "pseudo_identity": self.pseudo_identity,
            "password": self.password
        }
        
        response = requests.post(f"{self.base_url}/authenticate", json=auth_data)
        if response.status_code == 200:
            data = response.json()
            self.session_key = data["session_key"]
            print("Authentication successful!")
            return True
        else:
            print(f"Authentication failed: {response.json()['error']}")
            return False
            
    def _generate_pseudo_identity(self, user_id):
        """Generate pseudo-identity using SHA-256"""
        import hashlib
        return hashlib.sha256(user_id.encode()).hexdigest()
    
    def encrypt_data(self, data):
        """Encrypt data using AES-GCM with the session key"""
        if not self.session_key:
            raise ValueError("Not authenticated. Call authenticate() first.")
            
        # Convert session key from hex to bytes
        key = bytes.fromhex(self.session_key)
        
        # Generate a random 96-bit nonce
        nonce = os.urandom(12)
        
        # Create an AES-GCM cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Convert data to bytes and encrypt
        data_bytes = json.dumps(data).encode()
        ciphertext = encryptor.update(data_bytes) + encryptor.finalize()
        
        return {
            "encrypted_data": ciphertext.hex(),
            "tag": encryptor.tag.hex(),
            "nonce": nonce.hex()
        }
    
    def send_data(self, data):
        """Send encrypted data to the server"""
        if not self.session_key:
            if not self.authenticate():
                return False
                
        encrypted = self.encrypt_data(data)
        payload = {
            "user_id": self.user_id,
            "encrypted_data": encrypted["encrypted_data"],
            "tag": encrypted["tag"],
            "nonce": encrypted["nonce"],
            "session_key": self.session_key
        }
        
        response = requests.post(f"{self.base_url}/data", json=payload)
        if response.status_code == 200:
            print("Data sent successfully!")
            print("Server response:", response.json())
            return True
        else:
            print(f"Failed to send data: {response.json()['error']}")
            return False
            
    def simulate_real_time_data(self, interval=5):
        """Simulate real-time WBAN data collection and transmission"""
        print(f"Starting real-time simulation (sending data every {interval} seconds)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                # Simulate various WBAN sensor readings
                data = {
                    "heart_rate": random.randint(60, 100),
                    "blood_pressure": {
                        "systolic": random.randint(110, 140),
                        "diastolic": random.randint(70, 90)
                    },
                    "temperature": round(random.uniform(36.5, 37.5), 1),
                    "blood_oxygen": random.randint(95, 100),
                    "timestamp": int(time.time())
                }
                
                print("\nSending data:", data)
                self.send_data(data)
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nSimulation stopped by user")

if __name__ == "__main__":
    # Example usage
    BASE_URL = "http://localhost:5000"  # Change this to your deployed server URL
    USER_ID = "user_1"  # Update this to match your registered user
    PASSWORD = "test123"  # Update this to match your registered user's password
    
    # Create simulator instance
    simulator = WBANDeviceSimulator(BASE_URL, USER_ID, PASSWORD)
    
    # Start real-time simulation
    simulator.simulate_real_time_data(interval=5)  # Send data every 5 seconds 