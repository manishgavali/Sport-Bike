from app import db
from datetime import datetime

class BikeSpec(db.Model):
    __tablename__ = 'bike_specs'
    
    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer, db.ForeignKey('bikes.id'), nullable=False, unique=True)
    
    # Engine Specifications
    engine_cc = db.Column(db.Integer)
    engine_type = db.Column(db.String(100))
    max_power = db.Column(db.Float)  # in HP
    max_power_rpm = db.Column(db.Integer)
    max_torque = db.Column(db.Float)  # in Nm
    max_torque_rpm = db.Column(db.Integer)
    fuel_system = db.Column(db.String(50))
    
    # Performance
    top_speed = db.Column(db.Float)  # in km/h
    acceleration_0_100 = db.Column(db.Float)  # in seconds
    mileage_city = db.Column(db.Float)  # in km/l
    mileage_highway = db.Column(db.Float)  # in km/l
    
    # Dimensions
    length = db.Column(db.Float)  # in mm
    width = db.Column(db.Float)  # in mm
    height = db.Column(db.Float)  # in mm
    wheelbase = db.Column(db.Float)  # in mm
    ground_clearance = db.Column(db.Float)  # in mm
    seat_height = db.Column(db.Float)  # in mm
    kerb_weight = db.Column(db.Float)  # in kg
    fuel_capacity = db.Column(db.Float)  # in liters
    
    # Brakes & Suspension
    front_brake = db.Column(db.String(100))
    rear_brake = db.Column(db.String(100))
    front_suspension = db.Column(db.String(100))
    rear_suspension = db.Column(db.String(100))
    
    # Tyres
    front_tyre = db.Column(db.String(50))
    rear_tyre = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BikeSpec for Bike ID {self.bike_id}>'
