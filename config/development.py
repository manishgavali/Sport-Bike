"""
Development environment specific configuration
Extended settings for local development
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import DevelopmentConfig as BaseDevConfig


class DevelopmentConfig(BaseDevConfig):
    """Extended development configuration with additional dev tools"""
    
    # Development database - use DATABASE_URL from .env
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data-dev.sqlite')
    
    # Enable SQL query profiling
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_QUERY_TIMEOUT = 0.5
    
    # Flask Debug Toolbar settings
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    
    # Development server settings
    SERVER_NAME = None  # Allow any hostname
    PREFERRED_URL_SCHEME = 'http'
    
    # Relaxed CORS for development
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', 'http://127.0.0.1:5000']
    
    # Development email - print to console
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = True
    
    # Seed data for development
    SEED_DATABASE = True
    
    # Hot reload templates
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = True
    
    # Development API keys (use test keys)
    WEATHER_API_KEY = os.environ.get('DEV_WEATHER_API_KEY', 'dev-test-key')
    MAPS_API_KEY = os.environ.get('DEV_MAPS_API_KEY', 'dev-test-key')
    
    # Mock blockchain for development
    BLOCKCHAIN_ENABLED = False
    
    # Development-specific features
    ENABLE_DEV_ROUTES = True
    ENABLE_API_DOCS = True
    
    # Local file storage
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'dev')


# Alias for backward compatibility
Config = DevelopmentConfig
