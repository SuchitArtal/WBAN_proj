from flask import Blueprint, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from app.utils.storage import users

data_bp = Blueprint("data", __name__)

@data_bp.route("/", methods=["POST"])
def send_data():
    try:
        data = request.json
        user_id = data.get("user_id")
        encrypted_data = data.get("encrypted_data")
        tag = data.get("tag")
        nonce = data.get("nonce")

        if not user_id or not encrypted_data or not tag or not nonce:
            return jsonify({"error": "Missing required fields"}), 400

        user_data = users.get(user_id)
        if not user_data:
            return jsonify({"error": "User not found"}), 404

        session_key = user_data.get("session_key")
        if not session_key:
            return jsonify({"error": "Session key not found"}), 400

        # Debugging logs
        print(f"Decrypting for user_id: {user_id}")
        print(f"Encrypted data: {encrypted_data}")
        print(f"Tag: {tag}, Nonce: {nonce}")
        print(f"Session key: {session_key}")

        cipher = Cipher(algorithms.AES(session_key), modes.GCM(bytes.fromhex(nonce), bytes.fromhex(tag)), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(bytes.fromhex(encrypted_data)) + decryptor.finalize()

        return jsonify({
            "message": "Data received successfully",
            "decrypted_data": decrypted_data.decode('utf-8')
        })

    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full error trace to logs
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
