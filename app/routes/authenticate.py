import hashlib
from flask import Blueprint, request, jsonify
from app.utils.storage import db, User, Session  # Ensure Session is correctly imported
from app import bcrypt, limiter
from app.utils.crypto import load_private_key, get_private_key_from_db
import os
import time
import base64

authenticate_bp = Blueprint("authenticate", __name__)

@authenticate_bp.route("", methods=["POST"])
@limiter.limit("5 per minute")  # Limit authentication attempts
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

        # Get the user's private key from database
        private_key_pem = get_private_key_from_db(user.user_id, db)
        if not private_key_pem:
            return jsonify({"error": "Private key not found"}), 500
        
        # Generate a random session key
        session_key = os.urandom(32)
        session_key_hex = session_key.hex()

        # Store session in DB
        new_session = Session(user_pseudo_identity=user.pseudo_identity, session_key=session_key_hex)
        db.session.add(new_session)
        db.session.commit()

        return jsonify({
            "message": "Authentication successful",
            "session_key": session_key_hex,
            "timestamp": timestamp  # Return the server-generated timestamp to the client
        }), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of failure
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
