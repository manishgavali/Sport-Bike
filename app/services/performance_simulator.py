import math

class PerformanceSimulator:
    """Simulates bike performance under various conditions"""
    
    def simulate_performance(self, bike, rider_weight, road_type, weather, riding_style):
        """Simulate performance based on conditions"""
        
        if not bike.specs:
            return {'error': 'Bike specifications not available'}
        
        # Base calculations
        total_weight = bike.specs.kerb_weight + rider_weight
        base_power = bike.specs.max_power
        base_torque = bike.specs.max_torque
        
        # Apply modifiers
        power_modifier = self._get_power_modifier(weather, road_type)
        style_modifier = self._get_style_modifier(riding_style)
        
        # Calculate adjusted performance
        adjusted_power = base_power * power_modifier
        adjusted_acceleration = self._calculate_acceleration(bike.specs, total_weight, adjusted_power)
        fuel_consumption = self._calculate_fuel_consumption(bike.specs, riding_style, road_type)
        heat_level = self._calculate_heat_level(riding_style, weather)
        wear_prediction = self._predict_component_wear(riding_style, road_type)
        
        return {
            'adjusted_power': round(adjusted_power, 2),
            'adjusted_acceleration': round(adjusted_acceleration, 2),
            'estimated_top_speed': round(bike.specs.top_speed * power_modifier, 2),
            'fuel_consumption': round(fuel_consumption, 2),
            'heat_level': heat_level,
            'brake_wear': wear_prediction['brake_wear'],
            'tyre_wear': wear_prediction['tyre_wear'],
            'chain_wear': wear_prediction['chain_wear'],
            'conditions': {
                'rider_weight': rider_weight,
                'total_weight': total_weight,
                'road_type': road_type,
                'weather': weather,
                'riding_style': riding_style
            }
        }
    
    def _get_power_modifier(self, weather, road_type):
        """Calculate power modifier based on conditions"""
        modifier = 1.0
        
        # Weather impact
        if weather == 'rainy':
            modifier *= 0.85
        elif weather == 'hot':
            modifier *= 0.95
        
        # Road type impact
        if road_type == 'city':
            modifier *= 0.90
        elif road_type == 'track':
            modifier *= 1.05
        
        return modifier
    
    def _get_style_modifier(self, riding_style):
        """Get riding style modifier"""
        modifiers = {
            'smooth': 0.85,
            'moderate': 1.0,
            'aggressive': 1.15
        }
        return modifiers.get(riding_style, 1.0)
    
    def _calculate_acceleration(self, specs, total_weight, adjusted_power):
        """Calculate adjusted 0-100 km/h time"""
        if not specs.acceleration_0_100:
            return 0
        
        # Simple physics-based calculation
        power_to_weight = adjusted_power / total_weight
        weight_factor = total_weight / specs.kerb_weight
        
        return specs.acceleration_0_100 * weight_factor / power_to_weight * 10
    
    def _calculate_fuel_consumption(self, specs, riding_style, road_type):
        """Calculate fuel consumption"""
        base_consumption = 100 / ((specs.mileage_city + specs.mileage_highway) / 2)
        
        # Style impact
        if riding_style == 'aggressive':
            base_consumption *= 1.3
        elif riding_style == 'smooth':
            base_consumption *= 0.85
        
        # Road type impact
        if road_type == 'city':
            base_consumption *= 1.2
        elif road_type == 'highway':
            base_consumption *= 0.9
        
        return base_consumption
    
    def _calculate_heat_level(self, riding_style, weather):
        """Calculate engine heat level"""
        heat = 50  # Base heat percentage
        
        if riding_style == 'aggressive':
            heat += 30
        elif riding_style == 'smooth':
            heat += 10
        
        if weather == 'hot':
            heat += 15
        elif weather == 'cold':
            heat -= 10
        
        return min(max(heat, 0), 100)
    
    def _predict_component_wear(self, riding_style, road_type):
        """Predict component wear rates"""
        base_wear = 1.0
        
        if riding_style == 'aggressive':
            brake_wear = base_wear * 1.5
            tyre_wear = base_wear * 1.4
            chain_wear = base_wear * 1.3
        elif riding_style == 'smooth':
            brake_wear = base_wear * 0.7
            tyre_wear = base_wear * 0.8
            chain_wear = base_wear * 0.85
        else:
            brake_wear = base_wear
            tyre_wear = base_wear
            chain_wear = base_wear
        
        if road_type == 'track':
            brake_wear *= 1.8
            tyre_wear *= 2.0
        
        return {
            'brake_wear': f"{round(brake_wear * 100)}%",
            'tyre_wear': f"{round(tyre_wear * 100)}%",
            'chain_wear': f"{round(chain_wear * 100)}%"
        }
