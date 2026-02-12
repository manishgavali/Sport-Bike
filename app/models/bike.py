from app import db
from datetime import datetime

class Bike(db.Model):
    __tablename__ = 'bikes'
    
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False, index=True)
    model = db.Column(db.String(100), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))  # sport, supersport, naked, touring
    image_url = db.Column(db.String(255))
    price = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    specs = db.relationship('BikeSpec', backref='bike', uselist=False, cascade='all, delete-orphan')
    user_bikes = db.relationship('UserBike', backref='bike', lazy='dynamic')
    reviews = db.relationship('Review', backref='bike', lazy='dynamic')
    
    def __repr__(self):
        return f'<Bike {self.brand} {self.model}>'
