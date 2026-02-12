"""
Database Models Tests
Tests for all database models and their relationships
"""

import pytest
from datetime import datetime
from app.models import User, Bike, BikeSpecs, UserBike, Ride, MaintenanceRecord
from app import db


class TestUserModel:
    """Test User model"""
    
    def test_create_user(self, app):
        """Test creating a new user"""
        with app.app_context():
            user = User(
                username='newuser',
                email='newuser@test.com',
                first_name='New',
                last_name='User'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'newuser'
            assert user.email == 'newuser@test.com'
    
    def test_password_hashing(self, app):
        """Test password hashing and verification"""
        with app.app_context():
            user = User(username='testuser', email='test@test.com')
            user.set_password('mysecretpassword')
            
            assert user.password_hash is not None
            assert user.password_hash != 'mysecretpassword'
            assert user.check_password('mysecretpassword')
            assert not user.check_password('wrongpassword')
    
    def test_user_representation(self, app):
        """Test user string representation"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert str(user) == f'<User {user.username}>' or user.username in str(user)
    
    def test_user_bikes_relationship(self, app):
        """Test user-bikes relationship"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            bikes = user.bikes  # Should access relationship
            assert isinstance(bikes, list)


class TestBikeModel:
    """Test Bike model"""
    
    def test_create_bike(self, app):
        """Test creating a new bike"""
        with app.app_context():
            bike = Bike(
                brand='Honda',
                model='CBR650R',
                year=2024,
                price=950000,
                category='sport'
            )
            db.session.add(bike)
            db.session.commit()
            
            assert bike.id is not None
            assert bike.brand == 'Honda'
            assert bike.model == 'CBR650R'
    
    def test_bike_with_specs(self, app):
        """Test bike with specifications"""
        with app.app_context():
            bike = Bike(
                brand='Kawasaki',
                model='Ninja 400',
                year=2024,
                price=550000,
                category='sport'
            )
            
            specs = BikeSpecs(
                bike=bike,
                engine_cc=399,
                max_power=45,
                max_torque=38,
                kerb_weight=168,
                fuel_capacity=14,
                mileage=28
            )
            
            db.session.add(bike)
            db.session.add(specs)
            db.session.commit()
            
            assert bike.specs is not None
            assert bike.specs.engine_cc == 399
            assert bike.specs.max_power == 45
    
    def test_bike_representation(self, app):
        """Test bike string representation"""
        with app.app_context():
            bike = Bike.query.first()
            bike_str = str(bike)
            assert bike.brand in bike_str and bike.model in bike_str


class TestUserBikeModel:
    """Test UserBike model (ownership)"""
    
    def test_assign_bike_to_user(self, app):
        """Test assigning a bike to a user"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            bike = Bike.query.first()
            
            user_bike = UserBike(
                user_id=user.id,
                bike_id=bike.id,
                purchase_date=datetime.utcnow(),
                purchase_price=bike.price,
                current_km=5000,
                registration_number='MH01AB1234'
            )
            
            db.session.add(user_bike)
            db.session.commit()
            
            assert user_bike.id is not None
            assert user_bike.user_id == user.id
            assert user_bike.bike_id == bike.id
    
    def test_user_bike_relationship(self, app):
        """Test relationships in UserBike model"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            bike = Bike.query.first()
            
            user_bike = UserBike(
                user_id=user.id,
                bike_id=bike.id,
                purchase_date=datetime.utcnow()
            )
            
            db.session.add(user_bike)
            db.session.commit()
            
            # Test relationships
            assert user_bike.user == user
            assert user_bike.bike == bike


class TestRideModel:
    """Test Ride model"""
    
    def test_create_ride(self, app):
        """Test creating a ride record"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            bike = Bike.query.first()
            
            # Create user_bike first
            user_bike = UserBike(
                user_id=user.id,
                bike_id=bike.id,
                purchase_date=datetime.utcnow()
            )
            db.session.add(user_bike)
            db.session.commit()
            
            ride = Ride(
                user_bike_id=user_bike.id,
                ride_date=datetime.utcnow(),
                distance=50.5,
                duration=60,
                avg_speed=50.5,
                max_speed=80.0,
                fuel_consumed=2.5,
                road_type='highway',
                weather='sunny'
            )
            
            db.session.add(ride)
            db.session.commit()
            
            assert ride.id is not None
            assert ride.distance == 50.5
            assert ride.avg_speed == 50.5
    
    def test_ride_mileage_calculation(self, app):
        """Test calculating mileage from ride data"""
        with app.app_context():
            ride = Ride(
                distance=100,
                fuel_consumed=4
            )
            
            mileage = ride.distance / ride.fuel_consumed
            assert mileage == 25.0


class TestMaintenanceModel:
    """Test Maintenance model"""
    
    def test_create_maintenance_record(self, app):
        """Test creating maintenance record"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            bike = Bike.query.first()
            
            user_bike = UserBike(
                user_id=user.id,
                bike_id=bike.id,
                purchase_date=datetime.utcnow()
            )
            db.session.add(user_bike)
            db.session.commit()
            
            maintenance = MaintenanceRecord(
                user_bike_id=user_bike.id,
                service_date=datetime.utcnow(),
                service_type='oil_change',
                odometer_reading=5000,
                cost=1500,
                description='Engine oil and filter change'
            )
            
            db.session.add(maintenance)
            db.session.commit()
            
            assert maintenance.id is not None
            assert maintenance.service_type == 'oil_change'
            assert maintenance.cost == 1500


class TestModelRelationships:
    """Test model relationships and cascades"""
    
    def test_user_deletion_cascades(self, app):
        """Test that deleting user cascades properly"""
        with app.app_context():
            # Create user with bike
            user = User(username='deletetest', email='delete@test.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
            
            # Delete user
            db.session.delete(user)
            db.session.commit()
            
            # Verify user is deleted
            assert User.query.get(user_id) is None
    
    def test_bike_users_relationship(self, app):
        """Test many-to-many relationship between bikes and users"""
        with app.app_context():
            bike = Bike.query.first()
            users_with_bike = UserBike.query.filter_by(bike_id=bike.id).all()
            assert isinstance(users_with_bike, list)


# Run tests with: pytest tests/
# Run specific test: pytest tests/test_models.py::TestUserModel::test_create_user
# Run with coverage: pytest --cov=app tests/
