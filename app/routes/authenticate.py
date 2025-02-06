from flask import Blueprint, request, jsonify
from cryptography.hazmat.primitives.asymmetric import ec
from app.utils.storage import users, bcrypt

authenticate_bp = Blueprint("authenticate", __name__)

@authenticate_bp.route("/", methods=["POST"])
def authenticate():
    try:
        # Parse the JSON input
        data = request.json
        user_id = data.get("user_id")
        password = data.get("password")
        pseudo_identity = data.get("pseudo_identity")
        signed_message = data.get("signed_message")  # Placeholder for signature validation

        # Validate inputs
        if not user_id or not password or not pseudo_identity:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if the user exists
        user_data = users.get(user_id)
        if not user_data:
            return jsonify({"error": "User not found"}), 404

        # Validate the password
        if not bcrypt.check_password_hash(user_data["hashed_password"], password):
            return jsonify({"error": "Invalid password"}), 401

        # Validate the pseudo-identity
        if user_data["pseudo_identity"] != pseudo_identity:
            return jsonify({"error": "Invalid pseudo_identity"}), 401

        # Placeholder for signature verification
        # In a real implementation, verify the signed_message using the user's public key

        # Generate a shared session key using ECDH
        private_key = user_data["private_key"]
        session_key = private_key.exchange(ec.ECDH(), user_data["public_key"])

        # Store the session key in the user's data
        user_data["session_key"] = session_key

        return jsonify({
            "message": "Authentication successful",
            "session_key": session_key.hex()  # Return the session key
        })

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
