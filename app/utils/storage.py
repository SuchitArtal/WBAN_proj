from flask_bcrypt import Bcrypt

# In-memory storage for users (for simplicity; consider using a database later)
users = {}

# Initialize Bcrypt
bcrypt = Bcrypt()
