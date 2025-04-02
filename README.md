# WBAN Authentication and Secure Data Transmission

A secure authentication and data transmission system for **Wireless Body Area Networks (WBAN)** using modern cryptographic techniques. This project ensures secure communication between WBAN devices and a server by implementing **ECC, AES-GCM, SHA-256, and bcrypt**.

## Features

### Completed Features
- **User Registration**: Generates pseudo-identity using SHA-256, and stores securely hashed passwords.
- **Authentication**: Validates user credentials and pseudo-identity, then establishes a secure session key.
- **Secure Data Transmission**: Uses **AES-GCM** encryption for transmitting sensitive WBAN data.
- **System Reset**: Allows administrators to **revoke all user data** when necessary.
- **PostgreSQL Integration**: Robust database storage for users and sessions.
- **Docker Support**: Containerized application with Docker and Docker Compose.
- **Structured API Responses**: Beautiful and well-formatted JSON responses with proper units and timestamps.

### Upcoming Features
- **ECC Key Management**: Implementation of Elliptic Curve Cryptography for public key generation.
- **Rate Limiting**: Protection against brute force and DDoS attacks.
- **Security Logging**: Comprehensive audit trails and security event monitoring.
- **Cloud Deployment**: Production-ready cloud deployment with proper security measures.

## System Architecture

The system consists of the following components:

- **Flask-based Backend**:
  - Built using Flask with modular design (Blueprints for endpoints).
  - Cryptographic operations handled using the `cryptography` library.
  - PostgreSQL database for persistent storage.
  - Docker containerization for easy deployment.

- **Endpoints**:
  - `/register`: Registers a new user.
  - `/authenticate`: Authenticates the user and establishes a session key.
  - `/data`: Accepts encrypted data, decrypts it, and validates authenticity.
  - `/revoke_all`: Deletes all stored user data.

- **Encryption Techniques**:
  - **AES-GCM**: Ensures encrypted and authenticated data transmission.
  - **SHA-256**: Derives pseudo-identities for added security.
  - **Bcrypt**: Hashes user passwords securely.

## Installation and Setup

### Prerequisites

Ensure you have the following installed:
- Docker and Docker Compose
- Git

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/SuchitArtal/WBAN_proj.git
   cd WBAN_proj
   ```

2. **Build and run with Docker**:
   ```sh
   docker-compose up --build -d
   ```

The application will be available at `http://localhost:5000`

## Database Access

To view the PostgreSQL database:
```sh
docker exec -it postgres_db psql -U postgres -d wban_db
```

Useful PostgreSQL commands:
```sql
-- List all tables
\dt

-- View users table
SELECT * FROM users;

-- View sessions table
SELECT * FROM sessions;

-- Exit psql
\q
```

## API Endpoints

### 1. Register User
**URL**: `/register`  
**Method**: `POST`  
**Request Body**:
```json
{
    "user_id": "user1",
    "password": "1234"
}
```
**Response**:
```json
{
    "message": "User registered successfully",
    "pseudo_identity": "<generated_pid>"
}
```

### 2. Authenticate User
**URL**: `/authenticate`  
**Method**: `POST`  
**Request Body**:
```json
{
    "pseudo_identity": "<generated_pid>",
    "password": "1234"
}
```
**Response**:
```json
{
    "message": "Authentication successful",
    "session_key": "<generated_session_key>"
}
```

### 3. Send Encrypted Data
**URL**: `/data`  
**Method**: `POST`  
**Request Body**:
```json
{
    "user_id": "user1",
    "encrypted_data": "<encrypted_payload>",
    "tag": "<gcm_tag>",
    "nonce": "<nonce>",
    "session_key": "<generated_session_key>"
}
```
**Response**:
```json
{
    "status": "success",
    "message": "Data received and decrypted successfully",
    "data": {
        "vital_signs": {
            "heart_rate": {
                "value": 75,
                "unit": "bpm"
            },
            "blood_pressure": {
                "systolic": {
                    "value": 120,
                    "unit": "mmHg"
                },
                "diastolic": {
                    "value": 80,
                    "unit": "mmHg"
                }
            },
            "temperature": {
                "value": 36.8,
                "unit": "°C"
            }
        },
        "metadata": {
            "timestamp": 1234567890,
            "formatted_time": "2024-03-31 12:34:56"
        }
    }
}
```

### 4. Revoke All User Data
**URL**: `/revoke_all`  
**Method**: `POST`  
**Response**:
```json
{
    "message": "All users have been deleted"
}
```

## Security Measures

- **Mutual Authentication**: Users and the server verify each other's identities.
- **End-to-End Encryption**: AES-GCM encrypts data for confidentiality and integrity.
- **Password Protection**: Bcrypt securely hashes passwords before storing them.
- **Database Security**: PostgreSQL with proper access controls.
- **Containerization**: Isolated environments with Docker.

## Contributing

Contributions are welcome! Feel free to fork this repository, raise issues, and submit pull requests.

## License

This project is licensed under the **MIT License**.

## Contact

**Suchit B Artal**  
📧 [suchitartal.2020@gmail.com](mailto:suchitartal.2020@gmail.com)  
🔗 [GitHub](https://github.com/SuchitArtal) | [LinkedIn](https://linkedin.com/in/username)
