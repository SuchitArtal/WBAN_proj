-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(64) PRIMARY KEY,
    pseudo_identity VARCHAR(256) UNIQUE NOT NULL,
    hashed_password VARCHAR(256) NOT NULL,
    public_key TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_pseudo_identity VARCHAR(256) REFERENCES users(pseudo_identity) ON DELETE CASCADE,
    session_key VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing ECC keys
CREATE TABLE IF NOT EXISTS ecc_keys (
    user_id VARCHAR(64) PRIMARY KEY,
    private_key TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
); 