from app import db
from datetime import datetime

class ResalePrediction(db.Model):
    __tablename__ = 'resale_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer, db.ForeignKey('bikes.id'), nullable=False)
    
    purchase_price = db.Column(db.Float, nullable=False)
    years_old = db.Column(db.Integer, nullable=False)
    km_driven = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(20))  # excellent, good, fair, poor
    
    # Prediction Results
    predicted_value = db.Column(db.Float)
    depreciation_rate = db.Column(db.Float)
    market_demand = db.Column(db.String(20))  # high, medium, low
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ResalePrediction for Bike ID {self.bike_id}>'
