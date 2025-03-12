import hashlib
from flask import Blueprint, request, jsonify
from app.utils.storage import db, User
from app import bcrypt

register_bp = Blueprint("register", __name__)

@register_bp.route("", methods=["POST"])
def register():
    try:
        data = request.json
        user_id = data.get("user_id")  # Accept user_id instead of pseudo_identity
        password = data.get("password")

        if not user_id or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Generate ECC Key Pair (To Be Implemented)
        public_key = "Generated_Public_Key"

        # Generate Pseudo-Identity from user_id using SHA-256
        pseudo_identity = hashlib.sha256(user_id.encode()).hexdigest()

        # Check if user already exists
        existing_user = User.query.filter_by(user_id=user_id).first()
        if existing_user:
            return jsonify({"error": "User already registered"}), 400

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Store user in DB
        new_user = User(user_id=user_id, pseudo_identity=pseudo_identity,
                        hashed_password=hashed_password, public_key=public_key)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "pseudo_identity": pseudo_identity,
            "public_key": public_key
        }), 201

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
