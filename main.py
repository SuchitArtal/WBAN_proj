from app import app, db
from flask_migrate import Migrate
from app.utils.storage import init_db

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize database tables
init_db(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Debug mode enabled for development
