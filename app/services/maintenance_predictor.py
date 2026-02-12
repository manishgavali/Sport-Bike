from datetime import datetime, timedelta
from app.models.maintenance_records import MaintenanceRecord

class MaintenancePredictor:
    """Predicts maintenance needs using AI logic"""
    
    # Standard maintenance intervals (in km)
    MAINTENANCE_INTERVALS = {
        'engine_oil': 3000,
        'oil_filter': 3000,
        'air_filter': 6000,
        'spark_plug': 8000,
        'chain_lubrication': 500,
        'chain_replacement': 15000,
        'brake_pads_front': 12000,
        'brake_pads_rear': 15000,
        'brake_fluid': 8000,
        'coolant': 10000,
        'tyres': 20000,
        'battery': 30000
    }
    
    def predict_maintenance(self, user_bike):
        """Predict maintenance schedule for a bike"""
        current_km = user_bike.current_km
        predictions = []
        
        # Get last maintenance records
        last_records = self._get_last_maintenance_records(user_bike.id)
        
        for component, interval in self.MAINTENANCE_INTERVALS.items():
            last_service_km = self._get_last_service_km(component, last_records)
            km_since_service = current_km - last_service_km
            km_until_service = interval - km_since_service
            
            # Calculate urgency
            urgency = self._calculate_urgency(km_since_service, interval)
            
            # Estimate days until service (assuming 30 km/day average)
            days_until_service = max(0, km_until_service / 30)
            due_date = datetime.now() + timedelta(days=days_until_service)
            
            predictions.append({
                'component': component.replace('_', ' ').title(),
                'last_service_km': last_service_km,
                'current_km': current_km,
                'km_since_service': km_since_service,
                'km_until_service': max(0, km_until_service),
                'days_until_service': int(days_until_service),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'urgency': urgency,
                'status': self._get_status(urgency)
            })
        
        # Sort by urgency
        predictions.sort(key=lambda x: x['urgency'], reverse=True)
        
        return predictions
    
    def _get_last_maintenance_records(self, user_bike_id):
        """Get last maintenance records for a bike"""
        records = MaintenanceRecord.query.filter_by(
            user_bike_id=user_bike_id
        ).order_by(MaintenanceRecord.service_date.desc()).limit(20).all()
        
        return records
    
    def _get_last_service_km(self, component, records):
        """Get odometer reading from last service for specific component"""
        for record in records:
            if record.parts_replaced and component in record.parts_replaced.lower():
                return record.odometer_reading or 0
        return 0
    
    def _calculate_urgency(self, km_since_service, interval):
        """Calculate urgency score (0-100)"""
        percentage = (km_since_service / interval) * 100
        
        if percentage >= 100:
            return 100  # Overdue
        elif percentage >= 90:
            return 90   # Critical
        elif percentage >= 75:
            return 75   # High
        elif percentage >= 50:
            return 50   # Medium
        else:
            return 25   # Low
    
    def _get_status(self, urgency):
        """Get maintenance status"""
        if urgency >= 100:
            return 'overdue'
        elif urgency >= 90:
            return 'critical'
        elif urgency >= 75:
            return 'high'
        elif urgency >= 50:
            return 'medium'
        else:
            return 'low'
    
    def predict_next_major_service(self, user_bike):
        """Predict next major service"""
        current_km = user_bike.current_km
        major_service_interval = 6000  # Every 6000 km
        
        last_major_service = (current_km // major_service_interval) * major_service_interval
        next_major_service = last_major_service + major_service_interval
        km_until_service = next_major_service - current_km
        
        return {
            'next_service_km': next_major_service,
            'km_remaining': km_until_service,
            'estimated_cost': self._estimate_service_cost(user_bike.bike),
            'estimated_date': (datetime.now() + timedelta(days=km_until_service/30)).strftime('%Y-%m-%d')
        }
    
    def _estimate_service_cost(self, bike):
        """Estimate service cost based on bike type"""
        base_cost = 2000  # Base service cost in INR
        
        if bike.specs and bike.specs.engine_cc:
            # Higher CC = Higher service cost
            if bike.specs.engine_cc > 600:
                base_cost *= 2.5
            elif bike.specs.engine_cc > 400:
                base_cost *= 2.0
            elif bike.specs.engine_cc > 250:
                base_cost *= 1.5
        
        return base_cost
