class CostCalculator:
    """Calculates total ownership cost"""
    
    # Insurance rates (annual, in INR)
    INSURANCE_RATES = {
        'comprehensive': {
            'below_150cc': 2500,
            '150cc_to_350cc': 4500,
            '350cc_to_500cc': 8000,
            'above_500cc': 15000
        },
        'third_party': {
            'below_150cc': 800,
            '150cc_to_350cc': 1200,
            '350cc_to_500cc': 1800,
            'above_500cc': 2500
        }
    }
    
    def calculate_ownership_cost(self, bike, yearly_km, fuel_price, insurance_type):
        """Calculate total ownership cost"""
        
        if not bike.specs:
            return {'error': 'Bike specifications not available'}
        
        # Calculate annual costs
        fuel_cost = self._calculate_fuel_cost(bike.specs, yearly_km, fuel_price)
        insurance_cost = self._calculate_insurance(bike.specs.engine_cc, insurance_type)
        maintenance_cost = self._calculate_maintenance_cost(bike.specs, yearly_km)
        depreciation = self._calculate_depreciation(bike.price)
        
        # Registration and other costs
        registration = 5000  # One-time (amortized over 5 years)
        accessories = 10000  # Optional accessories per year
        
        total_annual_cost = (
            fuel_cost + 
            insurance_cost + 
            maintenance_cost + 
            depreciation + 
            registration / 5 + 
            accessories
        )
        
        cost_per_km = total_annual_cost / yearly_km if yearly_km > 0 else 0
        cost_per_month = total_annual_cost / 12
        
        return {
            'breakdown': {
                'fuel_cost': round(fuel_cost, 2),
                'insurance_cost': round(insurance_cost, 2),
                'maintenance_cost': round(maintenance_cost, 2),
                'depreciation': round(depreciation, 2),
                'registration_annual': round(registration / 5, 2),
                'accessories': round(accessories, 2)
            },
            'totals': {
                'annual_cost': round(total_annual_cost, 2),
                'monthly_cost': round(cost_per_month, 2),
                'cost_per_km': round(cost_per_km, 2)
            },
            'comparison': {
                'daily_cost': round(total_annual_cost / 365, 2),
                '5_year_cost': round(total_annual_cost * 5, 2)
            }
        }
    
    def _calculate_fuel_cost(self, specs, yearly_km, fuel_price):
        """Calculate annual fuel cost"""
        avg_mileage = (specs.mileage_city + specs.mileage_highway) / 2
        liters_needed = yearly_km / avg_mileage
        return liters_needed * fuel_price
    
    def _calculate_insurance(self, engine_cc, insurance_type):
        """Calculate insurance cost based on CC"""
        rates = self.INSURANCE_RATES.get(insurance_type, self.INSURANCE_RATES['comprehensive'])
        
        if engine_cc < 150:
            return rates['below_150cc']
        elif engine_cc <= 350:
            return rates['150cc_to_350cc']
        elif engine_cc <= 500:
            return rates['350cc_to_500cc']
        else:
            return rates['above_500cc']
    
    def _calculate_maintenance_cost(self, specs, yearly_km):
        """Calculate annual maintenance cost"""
        # Base maintenance cost
        base_cost = 5000
        
        # Adjust based on CC
        if specs.engine_cc > 500:
            base_cost *= 2.5
        elif specs.engine_cc > 300:
            base_cost *= 1.8
        elif specs.engine_cc > 200:
            base_cost *= 1.4
        
        # Additional cost based on km
        services_per_year = yearly_km / 3000  # Service every 3000 km
        service_cost = base_cost * services_per_year
        
        # Add parts replacement (tyres, brake pads, etc.)
        parts_cost = (yearly_km / 15000) * 8000  # Major parts every 15000 km
        
        return service_cost + parts_cost
    
    def _calculate_depreciation(self, purchase_price):
        """Calculate annual depreciation"""
        # Sport bikes depreciate ~15% per year
        return purchase_price * 0.15
