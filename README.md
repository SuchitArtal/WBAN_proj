# WBAN Authentication and Secure Data Transmission

A secure authentication and data transmission system for **Wireless Body Area Networks (WBAN)** using modern cryptographic techniques. This project ensures secure communication between WBAN devices and a server by implementing **ECC, AES-GCM, SHA-256, and bcrypt**.

## Features

- **User Registration**: Generates ECC key pairs, pseudo-identity using SHA-256, and stores securely hashed passwords.
- **Authentication**: Validates user credentials and pseudo-identity, then establishes a **secure ECC Diffie-Hellman session key**.
- **Secure Data Transmission**: Uses **AES-GCM** encryption for transmitting sensitive WBAN data.
- **System Reset**: Allows administrators to **revoke all user data** when necessary.
- **Modular API**: A Flask-based API with secure cryptographic operations.

## System Architecture

The system consists of the following components:

- **Flask-based Backend**:
  - Built using Flask with modular design (Blueprints for endpoints).
  - Cryptographic operations handled using the `cryptography` library.

- **Endpoints**:
  - `/register`: Registers a new user.
  - `/authenticate`: Authenticates the user and establishes a session key.
  - `/data`: Accepts encrypted data, decrypts it, and validates authenticity.
  - `/revoke_all`: Deletes all stored user data.

- **Encryption Techniques**:
  - **Elliptic Curve Cryptography (ECC)**: Used for generating key pairs and secure key exchange.
  - **AES-GCM**: Ensures encrypted and authenticated data transmission.
  - **SHA-256**: Derives pseudo-identities for added security.
  - **Bcrypt**: Hashes user passwords securely.

## Installation and Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- `pip` package manager
- Virtual environment (`venv`)

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/SuchitArtal/WBAN_proj.git
   cd WBAN_proj
   ```

2. **Create a virtual environment and activate it**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```sh
   python main.py
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
    "pseudo_identity": "<generated_pid>",
    "public_key": "<generated_public_key>"
}
```

---

### 2. Authenticate User
**URL**: `/authenticate`  
**Method**: `POST`  
**Request Body**:
```json
{
    "user_id": "user1",
    "password": "1234",
    "pseudo_identity": "<generated_pid>",
    "signed_message": "dummy_signature"
}
```
**Response**:
```json
{
    "message": "Authentication successful",
    "session_key": "<generated_session_key>"
}
```

---

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
    "message": "Data received successfully",
    "decrypted_data": "Heart rate: 75 bpm"
}
```

---

### 4. Revoke All User Data
**URL**: `/revoke_all`  
**Method**: `POST`  
**Response**:
```json
{
    "message": "All users have been deleted"
}
```

---

## Security Measures

- **Mutual Authentication**: Users and the server verify each other's identities.
- **End-to-End Encryption**: AES-GCM encrypts data for confidentiality and integrity.
- **Secure Key Management**: ECC ensures lightweight, secure key exchange.
- **Password Protection**: Bcrypt securely hashes passwords before storing them.

## Future Enhancements

- **Database Integration**: Replace in-memory storage with PostgreSQL.
- **Multi-Factor Authentication**: Add OTP-based verification.
- **Logging & Monitoring**: Implement security logs for better auditability.
- **Lightweight Cryptographic Optimization**: Enhance performance for WBAN devices.

---

## Contributing

Contributions are welcome! Feel free to fork this repository, raise issues, and submit pull requests.

## License

This project is licensed under the **MIT License**.

---

## Contact

**Suchit B Artal**  
📧 [suchitartal.2020@gmail.com](mailto:suchitartal.2020@gmail.com)  
🔗 [GitHub](https://github.com/SuchitArtal) | [LinkedIn](https://linkedin.com/in/username)
