from app.models.bike_specs import BikeSpec

class ComparisonEngine:
    """Engine for comparing sport bikes across multiple parameters"""
    
    def compare_bikes(self, bikes):
        """Compare multiple bikes and return detailed comparison data"""
        comparison_data = {
            'performance': self._compare_performance(bikes),
            'economy': self._compare_economy(bikes),
            'dimensions': self._compare_dimensions(bikes),
            'recommendations': self._generate_recommendations(bikes)
        }
        return comparison_data
    
    def _compare_performance(self, bikes):
        """Compare performance metrics"""
        performance = []
        
        for bike in bikes:
            if bike.specs:
                score = self._calculate_performance_score(bike.specs)
                performance.append({
                    'bike': bike,
                    'top_speed': bike.specs.top_speed,
                    'acceleration': bike.specs.acceleration_0_100,
                    'power': bike.specs.max_power,
                    'torque': bike.specs.max_torque,
                    'score': score
                })
        
        return sorted(performance, key=lambda x: x['score'], reverse=True)
    
    def _compare_economy(self, bikes):
        """Compare fuel economy and costs"""
        economy = []
        
        for bike in bikes:
            if bike.specs:
                avg_mileage = (bike.specs.mileage_city + bike.specs.mileage_highway) / 2
                economy.append({
                    'bike': bike,
                    'city_mileage': bike.specs.mileage_city,
                    'highway_mileage': bike.specs.mileage_highway,
                    'avg_mileage': avg_mileage,
                    'price': bike.price
                })
        
        return sorted(economy, key=lambda x: x['avg_mileage'], reverse=True)
    
    def _compare_dimensions(self, bikes):
        """Compare physical dimensions and weight"""
        dimensions = []
        
        for bike in bikes:
            if bike.specs:
                dimensions.append({
                    'bike': bike,
                    'weight': bike.specs.kerb_weight,
                    'seat_height': bike.specs.seat_height,
                    'fuel_capacity': bike.specs.fuel_capacity,
                    'wheelbase': bike.specs.wheelbase
                })
        
        return dimensions
    
    def _calculate_performance_score(self, specs):
        """Calculate overall performance score"""
        score = 0
        
        if specs.top_speed:
            score += (specs.top_speed / 300) * 30  # Max 30 points
        
        if specs.acceleration_0_100:
            score += (10 / specs.acceleration_0_100) * 30  # Max 30 points (lower is better)
        
        if specs.max_power:
            score += (specs.max_power / 200) * 20  # Max 20 points
        
        if specs.max_torque:
            score += (specs.max_torque / 150) * 20  # Max 20 points
        
        return round(score, 2)
    
    def _generate_recommendations(self, bikes):
        """Generate intelligent recommendations"""
        recommendations = {}
        
        if bikes:
            performance_sorted = sorted(bikes, 
                key=lambda b: b.specs.max_power if b.specs else 0, 
                reverse=True)
            
            economy_sorted = sorted(bikes,
                key=lambda b: (b.specs.mileage_city + b.specs.mileage_highway) / 2 if b.specs else 0,
                reverse=True)
            
            recommendations['best_performance'] = performance_sorted[0] if performance_sorted else None
            recommendations['best_economy'] = economy_sorted[0] if economy_sorted else None
            recommendations['best_track'] = performance_sorted[0] if performance_sorted else None
            recommendations['best_daily'] = economy_sorted[0] if economy_sorted else None
        
        return recommendations
