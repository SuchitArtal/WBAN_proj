from flask import Blueprint, jsonify
from app.utils.storage import db, User, Session

revoke_bp = Blueprint("revoke", __name__)

@revoke_bp.route("", methods=["POST"])
def revoke_all():
    try:
        # Delete all sessions and users
        db.session.query(Session).delete()  # Use the correct table name: sessions
        db.session.query(User).delete()  # Use the correct table name: users
        db.session.commit()

        return jsonify({"message": "All users and sessions have been deleted"}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of failure
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
