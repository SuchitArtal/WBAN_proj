import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

# Load PostgreSQL configuration from environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:postgres@db/wban_db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# Import models
from app.utils.storage import User, Session

# Create tables
with app.app_context():
    db.create_all()

# Import and register blueprints
from app.routes.register import register_bp
from app.routes.authenticate import authenticate_bp
from app.routes.data import data_bp
from app.routes.revoke import revoke_bp

app.register_blueprint(register_bp, url_prefix="/register")
app.register_blueprint(authenticate_bp, url_prefix="/authenticate")
app.register_blueprint(data_bp, url_prefix="/data")
app.register_blueprint(revoke_bp, url_prefix="/revoke_all")

@app.route("/")
def index():
    return "WBAN Authentication Prototype is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
