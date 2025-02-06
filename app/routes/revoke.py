from flask import Blueprint, jsonify
from app.utils.storage import users

revoke_bp = Blueprint("revoke", __name__)

@revoke_bp.route("/", methods=["POST"])
def revoke_all():
    try:
        users.clear()  # Clears all users
        return jsonify({"message": "All users have been deleted"}), 200
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
