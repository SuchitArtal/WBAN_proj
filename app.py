from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time

# Initialize Flask app
app = Flask(__name__)

# Error handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": str(e.description),
        "status_code": 429
    }), 429

@app.errorhandler(500)
def internal_error_handler(e):
    return jsonify({
        "error": "Internal server error",
        "message": str(e),
        "status_code": 500
    }), 500

@app.errorhandler(400)
def bad_request_handler(e):
    return jsonify({
        "error": "Bad request",
        "message": str(e),
        "status_code": 400
    }), 400

@app.errorhandler(401)
def unauthorized_handler(e):
    return jsonify({
        "error": "Unauthorized",
        "message": str(e),
        "status_code": 401
    }), 401

# Rate limiting configuration
def rate_limit_handler():
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Too many requests. Please try again later.",
        "status_code": 429
    }), 429

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    on_breach=rate_limit_handler
)

# Configure rate limits for specific endpoints
@app.before_request
def configure_rate_limits():
    if request.path.startswith('/register'):
        endpoint = 'register.register'
        limiter.limit("3 per hour")(app.view_functions[endpoint])
    elif request.path.startswith('/authenticate'):
        endpoint = 'authenticate.authenticate'
        limiter.limit("5 per minute")(app.view_functions[endpoint])
    elif request.path.startswith('/data'):
        endpoint = 'data.send_data'
        limiter.limit("10 per minute")(app.view_functions[endpoint])
    elif request.path.startswith('/get_data'):
        endpoint = 'data.get_data'
        limiter.limit("30 per minute")(app.view_functions[endpoint])

# Import blueprints
from app.routes.register import register_bp
from app.routes.authenticate import authenticate_bp
from app.routes.data import data_bp
from app.routes.revoke import revoke_bp

# Register blueprints
app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(authenticate_bp, url_prefix='/authenticate')
app.register_blueprint(data_bp, url_prefix='/data')
app.register_blueprint(revoke_bp, url_prefix='/revoke_all')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')