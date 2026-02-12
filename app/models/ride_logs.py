from app import db
from datetime import datetime

class RideLog(db.Model):
    __tablename__ = 'ride_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_bike_id = db.Column(db.Integer, db.ForeignKey('user_bikes.id'), nullable=False)
    
    ride_date = db.Column(db.DateTime, default=datetime.utcnow)
    distance = db.Column(db.Float)  # in km
    duration = db.Column(db.Integer)  # in minutes
    avg_speed = db.Column(db.Float)  # in km/h
    max_speed = db.Column(db.Float)  # in km/h
    fuel_consumed = db.Column(db.Float)  # in liters
    
    road_type = db.Column(db.String(20))  # city, highway, track
    weather_condition = db.Column(db.String(20))  # sunny, rainy, cloudy
    riding_style = db.Column(db.String(20))  # smooth, moderate, aggressive
    
    start_location = db.Column(db.String(100))
    end_location = db.Column(db.String(100))
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RideLog {self.ride_date}>'
