class SafetyAdvisor:
    """Provides AI-based safety tips and recommendations"""
    
    def generate_safety_tips(self, bike, rider_experience, bike_condition):
        """Generate personalized safety tips"""
        tips = {
            'general': [],
            'bike_specific': [],
            'experience_based': [],
            'condition_alerts': []
        }
        
        # General safety tips
        tips['general'] = [
            "Always wear a DOT-approved helmet",
            "Check tyre pressure before every ride",
            "Use both brakes progressively for better control",
            "Maintain safe following distance",
            "Be visible - use headlights during day"
        ]
        
        # Bike-specific tips
        if bike.specs:
            if bike.specs.max_power and bike.specs.max_power > 50:
                tips['bike_specific'].append(
                    f"High-power bike ({bike.specs.max_power}HP) - Throttle control is crucial"
                )
                tips['bike_specific'].append(
                    "Practice emergency braking in safe environment"
                )
            
            if bike.specs.top_speed and bike.specs.top_speed > 180:
                tips['bike_specific'].append(
                    "High-speed capability - Always respect speed limits"
                )
                tips['bike_specific'].append(
                    "Aerodynamic tuck reduces wind resistance at high speeds"
                )
            
            if bike.specs.seat_height and bike.specs.seat_height > 800:
                tips['bike_specific'].append(
                    f"Tall seat height ({bike.specs.seat_height}mm) - Practice low-speed maneuvers"
                )
        
        # Experience-based tips
        if rider_experience == 'beginner':
            tips['experience_based'] = [
                "Take a professional riding course",
                "Start with empty parking lots for practice",
                "Avoid riding in heavy traffic initially",
                "Practice slow-speed maneuvers regularly",
                "Don't ride beyond your skill level"
            ]
        elif rider_experience == 'intermediate':
            tips['experience_based'] = [
                "Practice advanced cornering techniques",
                "Learn proper body positioning",
                "Master trail braking on track",
                "Develop situational awareness",
                "Consider track day for skill improvement"
            ]
        else:  # expert
            tips['experience_based'] = [
                "Mentor new riders when possible",
                "Keep skills sharp with regular practice",
                "Stay updated on latest safety technology",
                "Share knowledge with community",
                "Lead by example in safe riding"
            ]
        
        # Condition-based alerts
        if bike_condition == 'poor':
            tips['condition_alerts'] = [
                "⚠️ URGENT: Poor bike condition detected",
                "Schedule immediate inspection",
                "Avoid long rides until serviced",
                "Check all critical systems before riding"
            ]
        elif bike_condition == 'fair':
            tips['condition_alerts'] = [
                "⚠️ Bike needs attention soon",
                "Schedule service within 1-2 weeks",
                "Monitor for unusual sounds or vibrations"
            ]
        
        return tips
    
    def check_safety_alerts(self, user_bike):
        """Check for safety alerts based on bike data"""
        alerts = []
        current_km = user_bike.current_km
        
        # High mileage alert
        if current_km > 50000:
            alerts.append({
                'type': 'warning',
                'title': 'High Mileage Alert',
                'message': f'{current_km} km - Increase maintenance frequency',
                'priority': 'medium'
            })
        
        # Check if overdue for service (simplified logic)
        if current_km % 3000 < 100:  # Within 100km of service interval
            alerts.append({
                'type': 'info',
                'title': 'Service Due Soon',
                'message': f'Next service due at {(current_km // 3000 + 1) * 3000} km',
                'priority': 'low'
            })
        
        # Weather-based alerts (can be enhanced with real API)
        alerts.append({
            'type': 'info',
            'title': 'Weather Advisory',
            'message': 'Check weather before long rides',
            'priority': 'low'
        })
        
        return alerts
    
    def get_riding_tips_by_weather(self, weather):
        """Get weather-specific riding tips"""
        tips = {
            'rainy': [
                "Reduce speed by 20-30%",
                "Increase following distance significantly",
                "Avoid painted road markings (slippery)",
                "Use both brakes gently",
                "Avoid sudden movements",
                "Watch for oil slicks and standing water"
            ],
            'sunny': [
                "Stay hydrated - carry water",
                "Use sunglasses or tinted visor",
                "Watch for heat exhaustion symptoms",
                "Tyre pressure increases in heat"
            ],
            'cold': [
                "Warm up bike longer",
                "Dress in layers",
                "Tyres take longer to warm up",
                "Watch for ice in shaded areas"
            ],
            'foggy': [
                "Use low beam headlights",
                "Reduce speed significantly",
                "Use road edges as guide",
                "Increase following distance"
            ]
        }
        
        return tips.get(weather, tips['sunny'])
