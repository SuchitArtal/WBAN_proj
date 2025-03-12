from app import db  # Import db from init.py

class User(db.Model):
    user_id = db.Column(db.String(64), primary_key=True)  # Primary Key
    hashed_password = db.Column(db.String(256), nullable=False)
    pseudo_identity = db.Column(db.String(64), unique=True, nullable=False)
    public_key = db.Column(db.Text, nullable=False)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_id = db.Column(db.String(64), db.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    session_key = db.Column(db.String(256), nullable=False)  # Secure session key
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


def init_db(app):
    """Initialize the database within the app context."""
    with app.app_context():
        db.create_all()
