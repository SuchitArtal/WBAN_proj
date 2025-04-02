import hashlib
from flask import Blueprint, request, jsonify
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from app.utils.storage import db, User, Session  # Ensure Session is correctly imported
from app import bcrypt
import os
import time

authenticate_bp = Blueprint("authenticate", __name__)

@authenticate_bp.route("", methods=["POST"])
def authenticate():
    try:
        data = request.json
        pseudo_identity = data.get("pseudo_identity")
        password = data.get("password")
        
        if not pseudo_identity or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Generate current timestamp server-side
        timestamp = int(time.time())

        # Retrieve user from database
        user = User.query.filter_by(pseudo_identity=pseudo_identity).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Validate password
        if not bcrypt.check_password_hash(user.hashed_password, password):
            return jsonify({"error": "Invalid password"}), 401

        # Generate ECC private key
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()

        # Compute session key using ECDH key exchange
        session_key = private_key.exchange(ec.ECDH(), public_key)

        # Convert session key to a hex string for storage
        session_key_hex = session_key.hex()

        # Store session in DB with correct column name
        new_session = Session(user_pseudo_identity=user.pseudo_identity, session_key=session_key_hex)
        db.session.add(new_session)
        db.session.commit()

        return jsonify({
            "message": "Authentication successful",
            "session_key": session_key_hex,
            "timestamp": timestamp  # Return the server-generated timestamp to the client
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
