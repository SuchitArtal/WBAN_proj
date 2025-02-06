from flask import Flask
from flask_bcrypt import Bcrypt

# Import blueprints
from app.routes.register import register_bp
from app.routes.authenticate import authenticate_bp
from app.routes.data import data_bp
from app.routes.revoke import revoke_bp  # Ensure this is included

# Initialize Flask app
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Register blueprints with URL prefixes
app.register_blueprint(register_bp, url_prefix="/register")
app.register_blueprint(authenticate_bp, url_prefix="/authenticate")
app.register_blueprint(data_bp, url_prefix="/data")
app.register_blueprint(revoke_bp, url_prefix="/revoke_all")  # Ensure this is registered

@app.route("/")
def index():
    return "WBAN Authentication Prototype is running!"
