from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey('bikes.id'), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Rating Categories
    performance_rating = db.Column(db.Integer)  # 1-5
    comfort_rating = db.Column(db.Integer)  # 1-5
    mileage_rating = db.Column(db.Integer)  # 1-5
    looks_rating = db.Column(db.Integer)  # 1-5
    
    ownership_duration = db.Column(db.String(50))  # 1 month, 6 months, 1 year, etc.
    km_driven = db.Column(db.Integer)
    
    pros = db.Column(db.Text)
    cons = db.Column(db.Text)
    images = db.Column(db.Text)  # JSON string of image URLs
    
    is_verified = db.Column(db.Boolean, default=False)
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.title}>'
