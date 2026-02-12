from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please login to access this page.'
    
    # Import models to register user_loader
    from app.models import user
    
    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.comparison import comparison_bp
    from app.blueprints.simulator import simulator_bp
    from app.blueprints.maintenance import maintenance_bp
    from app.blueprints.safety import safety_bp
    from app.blueprints.calculator import calculator_bp
    from app.blueprints.reports import reports_bp
    from app.blueprints.resale import resale_bp
    from app.blueprints.community import community_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(comparison_bp, url_prefix='/comparison')
    app.register_blueprint(simulator_bp, url_prefix='/simulator')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance')
    app.register_blueprint(safety_bp, url_prefix='/safety')
    app.register_blueprint(calculator_bp, url_prefix='/calculator')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(resale_bp, url_prefix='/resale')
    app.register_blueprint(community_bp, url_prefix='/community')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Home route
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('base.html')
    
    return app
