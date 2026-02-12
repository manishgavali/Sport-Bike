"""
Test package for Smart Sport Bike Ecosystem
Provides common fixtures and utilities for testing
"""

import os
import tempfile
import pytest
from app import create_app, db
from app.models import User, Bike, UserBike, Ride


@pytest.fixture(scope='session')
def app():
    """Create and configure a test application instance"""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        _seed_test_data()
        yield app
        db.drop_all()
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    """Test client for making requests"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """Database session that rolls back after each test"""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Bind session to connection
        session = db.create_scoped_session(
            options={'bind': connection, 'binds': {}}
        )
        db.session = session
        
        yield session
        
        transaction.rollback()
        connection.close()
        session.remove()


def _seed_test_data():
    """Seed database with test data"""
    from app.models import User, Bike, BikeSpecs
    
    # Create test user
    test_user = User(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    test_user.set_password('testpass123')
    db.session.add(test_user)
    
    # Create test bikes
    test_bike_1 = Bike(
        brand='Yamaha',
        model='R15 V4',
        year=2024,
        price=185000,
        category='sport'
    )
    
    test_bike_specs_1 = BikeSpecs(
        bike=test_bike_1,
        engine_cc=155,
        max_power=18.4,
        max_torque=14.2,
        kerb_weight=142,
        fuel_capacity=11,
        mileage=45
    )
    
    test_bike_2 = Bike(
        brand='KTM',
        model='Duke 390',
        year=2024,
        price=295000,
        category='naked'
    )
    
    test_bike_specs_2 = BikeSpecs(
        bike=test_bike_2,
        engine_cc=373,
        max_power=43.5,
        max_torque=37,
        kerb_weight=167,
        fuel_capacity=13.4,
        mileage=30
    )
    
    db.session.add_all([test_bike_1, test_bike_specs_1, test_bike_2, test_bike_specs_2])
    db.session.commit()


# Test user credentials
TEST_USER_EMAIL = 'test@example.com'
TEST_USER_PASSWORD = 'testpass123'
TEST_USER_USERNAME = 'testuser'
