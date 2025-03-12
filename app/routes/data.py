from flask import Blueprint, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from app.utils.storage import db, User, Session

data_bp = Blueprint("data", __name__)

@data_bp.route("", methods=["POST"])
def send_data():
    try:
        data = request.json
        pseudo_identity = data.get("pseudo_identity")
        encrypted_data = data.get("encrypted_data")
        tag = data.get("tag")
        nonce = data.get("nonce")

        if not pseudo_identity or not encrypted_data or not tag or not nonce:
            return jsonify({"error": "Missing required fields"}), 400

        # Retrieve session key from DB
        session = Session.query.filter_by(user_pid=pseudo_identity).first()
        if not session:
            return jsonify({"error": "Session not found"}), 404

        session_key = bytes.fromhex(session.session_key)

        # Decrypt data
        cipher = Cipher(algorithms.AES(session_key), modes.GCM(bytes.fromhex(nonce), bytes.fromhex(tag)), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(bytes.fromhex(encrypted_data)) + decryptor.finalize()

        return jsonify({"message": "Data received successfully", "decrypted_data": decrypted_data.decode('utf-8')}), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
