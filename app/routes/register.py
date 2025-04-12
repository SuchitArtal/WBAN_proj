import hashlib
from flask import Blueprint, request, jsonify
from app.utils.storage import db, User, ECCKey  # Import User model, database, and ECCKey model
from app import bcrypt, limiter
from app.utils.crypto import generate_ecc_key_pair

register_bp = Blueprint("register", __name__)

@register_bp.route("", methods=["POST"])
@limiter.limit("3 per hour")  # Limit new user registrations
def register():
    try:
        data = request.json
        user_id = data.get("user_id")  # Accept user_id instead of pseudo_identity
        password = data.get("password")

        if not user_id or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Generate Pseudo-Identity using SHA-256
        pseudo_identity = hashlib.sha256(user_id.encode()).hexdigest()

        # Check if user already exists
        existing_user = User.query.filter_by(user_id=user_id).first()
        if existing_user:
            return jsonify({"error": "User already registered"}), 400

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Generate ECC key pair
        private_key_pem, public_key_pem = generate_ecc_key_pair()

        # Create new user object
        new_user = User(
            user_id=user_id,
            pseudo_identity=pseudo_identity,
            hashed_password=hashed_password,
            public_key=public_key_pem
        )

        # Add user to the database and commit
        db.session.add(new_user)
        db.session.commit()  # Commit the user first to satisfy the foreign key constraint

        # Save the private key in the ECCKey table
        new_ecc_key = ECCKey(
            user_id=user_id,
            private_key=private_key_pem
        )

        # Add ECC key to the database
        db.session.add(new_ecc_key)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id,
            "pseudo_identity": pseudo_identity,
            "public_key": public_key_pem
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of failure
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
