from app import db
from datetime import datetime

class UserBike(db.Model):
    __tablename__ = 'user_bikes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey('bikes.id'), nullable=False)
    
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Float)
    current_km = db.Column(db.Integer, default=0)
    registration_number = db.Column(db.String(20), unique=True)
    bike_condition = db.Column(db.String(20), default='good')  # excellent, good, fair, poor
    
    # Customization
    modifications = db.Column(db.Text)
    bike_images = db.Column(db.Text)  # JSON string of image URLs
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ride_logs = db.relationship('RideLog', backref='user_bike', lazy='dynamic', cascade='all, delete-orphan')
    maintenance_records = db.relationship('MaintenanceRecord', backref='user_bike', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<UserBike {self.registration_number}>'
