from flask import Blueprint, request, jsonify
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from app.utils.storage import users, bcrypt

register_bp = Blueprint("register", __name__)

@register_bp.route("/", methods=["POST"])
def register():
    try:
        # Parse the JSON input
        data = request.json
        user_id = data.get("user_id")
        password = data.get("password")

        # Validate inputs
        if not user_id or not password:
            return jsonify({"error": "user_id and password are required"}), 400

        # Check if the user is already registered
        if user_id in users:
            return jsonify({"error": "User already registered"}), 400

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Generate ECC key pair
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()

        # Derive pseudo-identity (PID) using SHA256
        pid = hashes.Hash(hashes.SHA256())
        pid.update(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
        pseudo_identity = pid.finalize().hex()

        # Store user data
        users[user_id] = {
            "private_key": private_key,
            "public_key": public_key,
            "pseudo_identity": pseudo_identity,
            "hashed_password": hashed_password,
        }

        return jsonify({
            "message": "User registered successfully",
            "pseudo_identity": pseudo_identity,
            "public_key": public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
        })

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
