from flask import Blueprint, jsonify
from app.utils.storage import db, User, Session

revoke_bp = Blueprint("revoke", __name__)

@revoke_bp.route("", methods=["POST"])
def revoke_all():
    try:
        # Delete all users and sessions
        db.session.query(Session).delete()
        db.session.query(User).delete()
        db.session.commit()

        return jsonify({"message": "All users and sessions have been deleted"}), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
