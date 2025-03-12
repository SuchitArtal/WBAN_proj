from flask import Blueprint, request, jsonify
from cryptography.hazmat.primitives.asymmetric import ec
from app.utils.storage import db, User, Session  # Remove bcrypt
from app import bcrypt  # Import bcrypt from __init__.py

authenticate_bp = Blueprint("authenticate", __name__)

@authenticate_bp.route("", methods=["POST"])
def authenticate():
    try:
        data = request.json
        pseudo_identity = data.get("pseudo_identity")
        password = data.get("password")

        if not pseudo_identity or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Retrieve user from database
        user = User.query.filter_by(pseudo_identity=pseudo_identity).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Validate password
        if not bcrypt.check_password_hash(user.hashed_password, password):
            return jsonify({"error": "Invalid password"}), 401

        # Generate session key using ECC
        private_key = ec.generate_private_key(ec.SECP256R1())
        session_key = private_key.exchange(ec.ECDH(), private_key.public_key())

        # Store session in DB
        new_session = Session(user_pid=user.pseudo_identity, session_key=session_key.hex(), expires_at=db.func.current_timestamp())
        db.session.add(new_session)
        db.session.commit()

        return jsonify({"message": "Authentication successful", "session_key": session_key.hex()}), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
