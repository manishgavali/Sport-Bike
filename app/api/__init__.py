"""
REST API Module
Provides JSON endpoints for external integrations and mobile apps
"""

from flask import Blueprint

# API Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Import routes after blueprint creation to avoid circular imports
from app.api import bikes_api, user_api, analytics_api
