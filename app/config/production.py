import os
from urllib.parse import quote_plus

class ProductionConfig:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_production_secret_key')
    
    # Database Configuration with proper error handling
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', 'your_secure_password'))
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'wban_db')
    
    # Construct database URL with proper escaping
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'pool_pre_ping': True
    }
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = "200 per day;50 per hour" 