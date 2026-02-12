from app import db
from datetime import datetime

class MaintenanceRecord(db.Model):
    __tablename__ = 'maintenance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_bike_id = db.Column(db.Integer, db.ForeignKey('user_bikes.id'), nullable=False)
    
    maintenance_type = db.Column(db.String(50), nullable=False)  # service, repair, parts_replacement
    service_date = db.Column(db.Date, nullable=False)
    odometer_reading = db.Column(db.Integer)
    
    # Service Details
    description = db.Column(db.Text)
    parts_replaced = db.Column(db.Text)  # JSON string
    cost = db.Column(db.Float)
    service_center = db.Column(db.String(100))
    
    # Next Service Prediction
    next_service_km = db.Column(db.Integer)
    next_service_date = db.Column(db.Date)
    
    invoice_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MaintenanceRecord {self.maintenance_type} on {self.service_date}>'
