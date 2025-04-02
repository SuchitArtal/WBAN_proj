from app import app, db
from app.utils.storage import User, Session

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!") 