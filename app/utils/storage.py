from app import db  # Import db from __init__.py

class User(db.Model):
    """User model for storing user information."""
    user_id = db.Column(db.String(64), primary_key=True)  # Primary Key
    hashed_password = db.Column(db.String(256), nullable=False)
    pseudo_identity = db.Column(db.String(256), unique=True, nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    private_key = db.Column(db.Text, nullable=False)  # Add private key column

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_pseudo_identity = db.Column(db.String(256), db.ForeignKey("user.pseudo_identity", ondelete="CASCADE"), nullable=False)
    session_key = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

def init_db(app):
    """Initialize the database within the app context."""
    with app.app_context():
        db.create_all() 