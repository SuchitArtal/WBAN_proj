import requests
import time
import json
from datetime import datetime
import uuid

BASE_URL = "http://localhost:5000"

def generate_unique_username(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def test_registration_limit():
    print("\nTesting Registration Rate Limit (3 per hour)...")
    for i in range(4):  # Try to register 4 users
        data = {
            "user_id": generate_unique_username("test_user"),
            "password": "test123"
        }
        response = requests.post(f"{BASE_URL}/register", json=data)
        print(f"Registration attempt {i+1}: Status {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except requests.exceptions.JSONDecodeError:
            print(f"Response: {response.text}")
        time.sleep(1)  # Wait 1 second between attempts

def test_authentication_limit():
    print("\nTesting Authentication Rate Limit (5 per minute)...")
    try:
        # First register a test user
        test_user = generate_unique_username("rate_test_user")
        register_data = {
            "user_id": test_user,
            "password": "test123"
        }
        print(f"\nRegistering test user: {test_user}")
        response = requests.post(f"{BASE_URL}/register", json=register_data)
        print(f"Registration for auth test: Status {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            pseudo_identity = response.json()["pseudo_identity"]
            print(f"Got pseudo_identity: {pseudo_identity}")
            
            # Now try to authenticate multiple times
            auth_data = {
                "pseudo_identity": pseudo_identity,
                "password": "test123"
            }
            
            print("\nStarting authentication attempts...")
            for i in range(6):  # Try to authenticate 6 times
                print(f"\nAuthentication attempt {i+1}:")
                print(f"Request data: {auth_data}")
                response = requests.post(f"{BASE_URL}/authenticate", json=auth_data)
                print(f"Status: {response.status_code}")
                try:
                    print(f"Response: {response.json()}")
                except requests.exceptions.JSONDecodeError:
                    print(f"Raw response: {response.text}")
                time.sleep(1)  # Wait 1 second between attempts
        else:
            print("Failed to register test user for authentication test")
    except Exception as e:
        print(f"Error in authentication test: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

def test_data_transmission_limit():
    print("\nTesting Data Transmission Rate Limit (10 per minute)...")
    try:
        # First register and authenticate a test user
        test_user = generate_unique_username("data_test_user")
        register_data = {
            "user_id": test_user,
            "password": "test123"
        }
        print(f"\nRegistering test user: {test_user}")
        response = requests.post(f"{BASE_URL}/register", json=register_data)
        print(f"Registration for data test: Status {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            pseudo_identity = response.json()["pseudo_identity"]
            print(f"Got pseudo_identity: {pseudo_identity}")
            
            # Authenticate to get session key
            auth_data = {
                "pseudo_identity": pseudo_identity,
                "password": "test123"
            }
            print("\nAuthenticating user...")
            response = requests.post(f"{BASE_URL}/authenticate", json=auth_data)
            print(f"Authentication for data test: Status {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                session_key = response.json()["session_key"]
                print(f"Got session key: {session_key}")
                
                # Try to send data multiple times
                print("\nStarting data transmission attempts...")
                for i in range(11):  # Try to send 11 data points
                    data = {
                        "user_id": test_user,
                        "encrypted_data": "0123456789abcdef",  # Sample hex data
                        "tag": "0123456789abcdef",  # Sample hex tag
                        "nonce": "0123456789abcdef",  # Sample hex nonce
                        "session_key": session_key
                    }
                    print(f"\nData transmission attempt {i+1}:")
                    print(f"Request data: {data}")
                    response = requests.post(f"{BASE_URL}/data", json=data)
                    print(f"Status: {response.status_code}")
                    try:
                        print(f"Response: {response.json()}")
                    except requests.exceptions.JSONDecodeError:
                        print(f"Raw response: {response.text}")
                    time.sleep(0.5)  # Wait 0.5 seconds between attempts
            else:
                print("Failed to authenticate for data test")
        else:
            print("Failed to register test user for data test")
    except Exception as e:
        print(f"Error in data transmission test: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    print(f"Starting rate limit tests at {datetime.now()}")
    
    try:
        # Test registration limit
        test_registration_limit()
        
        # Wait a bit before testing authentication
        time.sleep(2)
        
        # Test authentication limit
        test_authentication_limit()
        
        # Wait a bit before testing data transmission
        time.sleep(2)
        
        # Test data transmission limit
        test_data_transmission_limit()
    except Exception as e:
        print(f"Error during test execution: {str(e)}")
    
    print(f"\nRate limit tests completed at {datetime.now()}") 