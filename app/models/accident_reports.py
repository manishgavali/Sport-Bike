from app import db
from datetime import datetime

class AccidentReport(db.Model):
    __tablename__ = 'accident_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey('bikes.id'), nullable=False)
    
    incident_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    severity = db.Column(db.String(20))  # minor, moderate, severe
    
    # Incident Details
    incident_type = db.Column(db.String(50))  # accident, breakdown, theft
    description = db.Column(db.Text, nullable=False)
    weather_condition = db.Column(db.String(20))
    road_condition = db.Column(db.String(20))
    
    # Damages
    damage_description = db.Column(db.Text)
    estimated_cost = db.Column(db.Float)
    images = db.Column(db.Text)  # JSON string of image URLs
    
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AccidentReport {self.incident_type} on {self.incident_date}>'
