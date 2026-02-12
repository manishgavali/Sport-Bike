class ResalePredictor:
    """Predicts resale value using ML-like logic"""
    
    # Depreciation rates by condition
    CONDITION_MULTIPLIER = {
        'excellent': 0.85,
        'good': 0.75,
        'fair': 0.60,
        'poor': 0.40
    }
    
    def predict_resale_value(self, bike, purchase_price, years_old, km_driven, condition):
        """Predict resale value"""
        
        # Base depreciation (15% per year for first 3 years)
        if years_old <= 3:
            age_depreciation = 1 - (0.15 * years_old)
        else:
            # 10% per year after 3 years
            age_depreciation = 0.55 - (0.10 * (years_old - 3))
        
        # Km-based depreciation
        km_factor = self._calculate_km_factor(km_driven, years_old)
        
        # Condition multiplier
        condition_factor = self.CONDITION_MULTIPLIER.get(condition, 0.70)
        
        # Brand value retention (some brands hold value better)
        brand_factor = self._get_brand_factor(bike.brand)
        
        # Calculate predicted value
        predicted_value = (
            purchase_price * 
            age_depreciation * 
            km_factor * 
            condition_factor * 
            brand_factor
        )
        
        # Calculate depreciation
        total_depreciation = purchase_price - predicted_value
        depreciation_percentage = (total_depreciation / purchase_price) * 100
        
        # Market demand analysis
        market_demand = self._analyze_market_demand(bike, years_old)
        
        return {
            'predicted_value': round(predicted_value, 2),
            'purchase_price': purchase_price,
            'total_depreciation': round(total_depreciation, 2),
            'depreciation_percentage': round(depreciation_percentage, 2),
            'factors': {
                'age_factor': round(age_depreciation * 100, 2),
                'km_factor': round(km_factor * 100, 2),
                'condition_factor': round(condition_factor * 100, 2),
                'brand_factor': round(brand_factor * 100, 2)
            },
            'market_analysis': market_demand,
            'selling_tips': self._get_selling_tips(condition, years_old)
        }
    
    def _calculate_km_factor(self, km_driven, years_old):
        """Calculate depreciation based on km driven"""
        avg_km_per_year = km_driven / years_old if years_old > 0 else km_driven
        
        if avg_km_per_year < 5000:
            return 0.95  # Low usage, better value
        elif avg_km_per_year < 10000:
            return 0.90  # Normal usage
        elif avg_km_per_year < 15000:
            return 0.80  # High usage
        else:
            return 0.70  # Very high usage
    
    def _get_brand_factor(self, brand):
        """Brand value retention factor"""
        premium_brands = ['KTM', 'BMW', 'Kawasaki', 'Yamaha', 'Ducati']
        good_brands = ['Honda', 'Suzuki', 'Royal Enfield']
        
        brand_upper = brand.upper()
        
        if any(premium in brand_upper for premium in premium_brands):
            return 1.1  # Premium brands hold value better
        elif any(good in brand_upper for good in good_brands):
            return 1.0  # Good resale value
        else:
            return 0.9  # Average resale value
    
    def _analyze_market_demand(self, bike, years_old):
        """Analyze market demand"""
        if years_old <= 2:
            demand = 'high'
            description = 'Recent model with high demand'
        elif years_old <= 5:
            demand = 'medium'
            description = 'Good demand in used bike market'
        else:
            demand = 'low'
            description = 'Older model, limited buyers'
        
        return {
            'demand_level': demand,
            'description': description,
            'best_time_to_sell': 'March-April' if years_old <= 3 else 'Year-round'
        }
    
    def _get_selling_tips(self, condition, years_old):
        """Get tips to maximize resale value"""
        tips = [
            "Complete all pending maintenance",
            "Clean and detail the bike professionally",
            "Keep all service records ready",
            "Take high-quality photos"
        ]
        
        if condition in ['fair', 'poor']:
            tips.append("Consider minor repairs to improve condition")
            tips.append("Be transparent about issues")
        
        if years_old > 5:
            tips.append("Highlight any upgrades or modifications")
            tips.append("Emphasize low running costs")
        
        return tips
