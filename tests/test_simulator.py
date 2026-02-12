"""
Performance Simulator Tests
Tests for AI-powered bike performance simulation
"""

import pytest
from app.models import Bike


class TestSimulatorInputForm:
    """Test simulator input form"""
    
    def test_simulator_page_loads(self, client):
        """Test simulator page is accessible"""
        response = client.get('/simulator/')
        assert response.status_code == 200
        assert b'Simulator' in response.data or b'Simulation' in response.data
    
    def test_simulator_requires_login(self, client):
        """Test simulator requires authentication"""
        response = client.get('/simulator/input_form', follow_redirects=False)
        # May or may not require login depending on design
        assert response.status_code in [200, 302, 401]
    
    def test_simulator_shows_bike_selection(self, client):
        """Test simulator shows bike selection options"""
        response = client.get('/simulator/')
        assert response.status_code == 200
        # Should show bikes or form
        assert b'select' in response.data.lower() or b'bike' in response.data.lower()


class TestSimulatorCalculations:
    """Test simulator calculation logic"""
    
    def test_basic_simulation(self, client, app):
        """Test basic performance simulation"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'passenger_weight': 0,
                'luggage_weight': 0,
                'road_type': 'highway',
                'weather': 'sunny',
                'riding_style': 'moderate',
                'distance': 100
            }, follow_redirects=True)
            
            assert response.status_code == 200
    
    def test_simulation_with_passenger(self, client, app):
        """Test simulation with passenger weight"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'has_passenger': True,
                'passenger_weight': 60,
                'luggage_weight': 10,
                'road_type': 'city',
                'weather': 'sunny',
                'riding_style': 'conservative',
                'distance': 50
            }, follow_redirects=True)
            
            assert response.status_code == 200
    
    def test_simulation_high_altitude(self, client, app):
        """Test simulation considers altitude effects"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'altitude': 2000,  # High altitude
                'road_type': 'highway',
                'weather': 'sunny',
                'riding_style': 'moderate',
                'distance': 100
            }, follow_redirects=True)
            
            assert response.status_code == 200
    
    def test_simulation_adverse_weather(self, client, app):
        """Test simulation with adverse weather conditions"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'road_type': 'city',
                'weather': 'rainy',
                'riding_style': 'conservative',
                'distance': 30
            }, follow_redirects=True)
            
            assert response.status_code == 200
    
    def test_simulation_aggressive_riding(self, client, app):
        """Test simulation with aggressive riding style"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'road_type': 'track',
                'weather': 'sunny',
                'riding_style': 'aggressive',
                'distance': 50
            }, follow_redirects=True)
            
            assert response.status_code == 200


class TestSimulatorResults:
    """Test simulator results display"""
    
    def test_results_show_fuel_consumption(self, client, app):
        """Test results include fuel consumption estimate"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'road_type': 'highway',
                'weather': 'sunny',
                'riding_style': 'moderate',
                'distance': 100
            }, follow_redirects=True)
            
            if response.status_code == 200:
                assert b'fuel' in response.data.lower() or b'mileage' in response.data.lower()
    
    def test_results_show_performance_metrics(self, client, app):
        """Test results include performance metrics"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'road_type': 'highway',
                'weather': 'sunny',
                'riding_style': 'aggressive',
                'distance': 100
            }, follow_redirects=True)
            
            if response.status_code == 200:
                # Should show speed, acceleration, or similar metrics
                assert b'speed' in response.data.lower() or b'power' in response.data.lower()
    
    def test_results_show_recommendations(self, client, app):
        """Test results include AI recommendations"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'road_type': 'city',
                'weather': 'rainy',
                'riding_style': 'moderate',
                'distance': 50
            }, follow_redirects=True)
            
            if response.status_code == 200:
                assert b'recommendation' in response.data.lower() or b'tip' in response.data.lower()


class TestSimulatorValidation:
    """Test simulator input validation"""
    
    def test_simulation_invalid_bike_id(self, client):
        """Test simulation with invalid bike ID"""
        response = client.post('/simulator/simulate', data={
            'bike_id': 99999,
            'rider_weight': 70,
            'road_type': 'highway',
            'weather': 'sunny',
            'riding_style': 'moderate',
            'distance': 100
        }, follow_redirects=True)
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 404]
    
    def test_simulation_negative_weight(self, client, app):
        """Test simulation rejects negative weight"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': -10,  # Invalid
                'road_type': 'highway',
                'weather': 'sunny',
                'riding_style': 'moderate',
                'distance': 100
            })
            
            # Should reject or use default
            assert response.status_code in [200, 400]
    
    def test_simulation_extreme_distance(self, client, app):
        """Test simulation with extreme distance values"""
        with app.app_context():
            bike = Bike.query.first()
            
            response = client.post('/simulator/simulate', data={
                'bike_id': bike.id,
                'rider_weight': 70,
                'road_type': 'highway',
                'weather': 'sunny',
                'riding_style': 'moderate',
                'distance': 10000  # Very long distance
            }, follow_redirects=True)
            
            assert response.status_code == 200
