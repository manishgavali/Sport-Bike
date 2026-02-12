"""
Database Initialization Script
This script creates all database tables based on your models.
Run this after setting up your database connection.
"""

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.bike import Bike
from app.models.user_bikes import UserBike
from app.models.bike_specs import BikeSpec
from app.models.ride_logs import RideLog
from app.models.maintenance_records import MaintenanceRecord
from app.models.reviews import Review
from app.models.accident_reports import AccidentReport
from app.models.resale_predictions import ResalePrediction
from app.models.admin_logs import AdminLog

def init_database():
    """Initialize the database with all tables"""
    app = create_app('development')
    
    with app.app_context():
        print("Creating database tables...")
        
        # Drop all tables (use with caution in production!)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        print("- users")
        print("- bikes")
        print("- user_bikes")
        print("- bike_specs")
        print("- ride_logs")
        print("- maintenance_records")
        print("- reviews")
        print("- accident_reports")
        print("- resale_predictions")
        print("- admin_logs")
        
        # Check if we need to create a default admin user
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            print("\n⚠️  No admin user found. Creating default admin...")
            admin_user = User(
                username='admin',
                email='admin@sportbike.com',
                full_name='System Administrator',
                role='admin',
                is_active=True
            )
            admin_user.set_password('admin123')  # Change this password!
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Default admin user created!")
            print("   Username: admin")
            print("   Password: admin123")
            print("   ⚠️  PLEASE CHANGE THIS PASSWORD AFTER FIRST LOGIN!")

if __name__ == '__main__':
    init_database()
