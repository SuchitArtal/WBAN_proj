from flask import Blueprint, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from app.utils.storage import db, User, Session
from app import limiter
import hashlib
import json
import time

data_bp = Blueprint("data", __name__)

@data_bp.route("", methods=["POST"])
@limiter.limit("10 per minute")  # Limit data transmission rate to 10 requests per minute
def send_data():
    try:
        data = request.json
        user_id = data.get("user_id")
        encrypted_data = data.get("encrypted_data")
        tag = data.get("tag")
        nonce = data.get("nonce")
        session_key = data.get("session_key")

        if not user_id or not encrypted_data or not tag or not nonce:
            return jsonify({"error": "Missing required fields"}), 400

        # Generate pseudo_identity from user_id
        pseudo_identity = hashlib.sha256(user_id.encode()).hexdigest()

        # Retrieve user from database
        user = User.query.filter_by(pseudo_identity=pseudo_identity).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # If session_key provided, use it directly
        if session_key:
            try:
                # Decrypt data using provided session key
                key = bytes.fromhex(session_key)
                nonce_bytes = bytes.fromhex(nonce)
                tag_bytes = bytes.fromhex(tag)
                cipher = Cipher(algorithms.AES(key), 
                              modes.GCM(nonce_bytes, tag_bytes),
                              backend=default_backend())
                decryptor = cipher.decryptor()
                encrypted_bytes = bytes.fromhex(encrypted_data)
                decrypted_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
                
                # Parse the decrypted JSON data
                decrypted_json = json.loads(decrypted_data.decode('utf-8'))
                
                # Format the response in a more structured way
                response = {
                    "status": "success",
                    "message": "Data received and decrypted successfully",
                    "data": {
                        "vital_signs": {
                            "heart_rate": {
                                "value": decrypted_json["heart_rate"],
                                "unit": "bpm"
                            },
                            "blood_pressure": {
                                "systolic": {
                                    "value": decrypted_json["blood_pressure"]["systolic"],
                                    "unit": "mmHg"
                                },
                                "diastolic": {
                                    "value": decrypted_json["blood_pressure"]["diastolic"],
                                    "unit": "mmHg"
                                }
                            },
                            "temperature": {
                                "value": decrypted_json["temperature"],
                                "unit": "°C"
                            }
                        },
                        "metadata": {
                            "timestamp": decrypted_json["timestamp"],
                            "formatted_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(decrypted_json["timestamp"]))
                        }
                    }
                }
                
                return jsonify(response), 200
            except Exception as e:
                return jsonify({"error": f"Decryption failed: {str(e)}"}), 400
        else:
            # If no session_key provided, look up in session table
            session = Session.query.filter_by(user_pseudo_identity=pseudo_identity).first()
            if not session:
                return jsonify({"error": "No active session found"}), 404

            try:
                # Decrypt data using session key from database
                key = bytes.fromhex(session.session_key)
                nonce_bytes = bytes.fromhex(nonce)
                tag_bytes = bytes.fromhex(tag)
                cipher = Cipher(algorithms.AES(key), 
                              modes.GCM(nonce_bytes, tag_bytes),
                              backend=default_backend())
                decryptor = cipher.decryptor()
                encrypted_bytes = bytes.fromhex(encrypted_data)
                decrypted_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
                
                # Parse the decrypted JSON data
                decrypted_json = json.loads(decrypted_data.decode('utf-8'))
                
                # Format the response in a more structured way
                response = {
                    "status": "success",
                    "message": "Data received and decrypted successfully",
                    "data": {
                        "vital_signs": {
                            "heart_rate": {
                                "value": decrypted_json["heart_rate"],
                                "unit": "bpm"
                            },
                            "blood_pressure": {
                                "systolic": {
                                    "value": decrypted_json["blood_pressure"]["systolic"],
                                    "unit": "mmHg"
                                },
                                "diastolic": {
                                    "value": decrypted_json["blood_pressure"]["diastolic"],
                                    "unit": "mmHg"
                                }
                            },
                            "temperature": {
                                "value": decrypted_json["temperature"],
                                "unit": "°C"
                            }
                        },
                        "metadata": {
                            "timestamp": decrypted_json["timestamp"],
                            "formatted_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(decrypted_json["timestamp"]))
                        }
                    }
                }
                
                return jsonify(response), 200
            except Exception as e:
                return jsonify({"error": f"Decryption failed: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
