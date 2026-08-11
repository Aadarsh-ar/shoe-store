import os
import tempfile
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key-change-me')
    
    # Detect if filesystem is read-only (e.g. Vercel Serverless) or if DATABASE_URL is provided
    db_env_url = os.getenv('DATABASE_URL')
    if not db_env_url:
        root_dir = os.path.dirname(basedir)
        # On Vercel / serverless platforms, root_dir is read-only. Fall back to tempfile directory (/tmp).
        if os.getenv('VERCEL') or os.getenv('VERCEL_ENV') or os.getenv('AWS_LAMBDA_FUNCTION_NAME') or not os.access(root_dir, os.W_OK):
            sqlite_file = os.path.join(tempfile.gettempdir(), 'shoestore.db')
        else:
            sqlite_file = os.path.join(root_dir, 'shoestore.db')
        db_env_url = f"sqlite:///{sqlite_file}"

    SQLALCHEMY_DATABASE_URI = db_env_url
    
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
