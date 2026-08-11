import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key-change-me')
    
    # Fallback SQLite database path - uses /tmp/ for Vercel serverless read-only environment
    default_db_dir = '/tmp' if os.getenv('VERCEL') or os.getenv('VERCEL_ENV') else os.path.dirname(basedir)
    default_sqlite = f"sqlite:///{os.path.join(default_db_dir, 'shoestore.db')}"
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default_sqlite)
    
    # Handle postgres:// vs postgresql:// if needed for Heroku/Render/Vercel Postgres URIs
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'images', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
