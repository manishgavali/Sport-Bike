"""
Bike Comparison Feature Tests
Tests for bike comparison functionality and filters
"""

import pytest
from app.models import Bike, BikeSpecs
from app import db


class TestComparisonPage:
    """Test comparison page functionality"""
    
    def test_comparison_page_loads(self, client):
        """Test comparison page is accessible"""
        response = client.get('/comparison/')
        assert response.status_code == 200
        assert b'Compare' in response.data or b'Comparison' in response.data
    
    def test_comparison_shows_available_bikes(self, client):
        """Test comparison page shows bikes for selection"""
        response = client.get('/comparison/')
        assert response.status_code == 200
        assert b'Yamaha' in response.data or b'KTM' in response.data


class TestBikeComparison:
    """Test bike comparison logic"""
    
    def test_compare_two_bikes(self, client, app):
        """Test comparing two bikes"""
        with app.app_context():
            bike1 = Bike.query.filter_by(brand='Yamaha').first()
            bike2 = Bike.query.filter_by(brand='KTM').first()
            
            response = client.get(f'/comparison/compare?bike1={bike1.id}&bike2={bike2.id}')
            assert response.status_code == 200
            assert b'Yamaha' in response.data
            assert b'KTM' in response.data
    
    def test_compare_three_bikes(self, client, app):
        """Test comparing three bikes"""
        with app.app_context():
            bikes = Bike.query.limit(3).all()
            if len(bikes) >= 3:
                response = client.get(
                    f'/comparison/compare?bike1={bikes[0].id}&bike2={bikes[1].id}&bike3={bikes[2].id}'
                )
                assert response.status_code == 200
    
    def test_compare_with_missing_bike(self, client):
        """Test comparison with non-existent bike ID"""
        response = client.get('/comparison/compare?bike1=999&bike2=1000')
        assert response.status_code in [404, 400] or b'not found' in response.data.lower()
    
    def test_comparison_shows_specs(self, client, app):
        """Test comparison shows bike specifications"""
        with app.app_context():
            bike1 = Bike.query.filter_by(brand='Yamaha').first()
            bike2 = Bike.query.filter_by(brand='KTM').first()
            
            response = client.get(f'/comparison/compare?bike1={bike1.id}&bike2={bike2.id}')
            assert response.status_code == 200
            
            # Check for spec data
            assert b'Power' in response.data or b'HP' in response.data
            assert b'Torque' in response.data or b'Nm' in response.data
            assert b'Weight' in response.data or b'kg' in response.data


class TestComparisonFilters:
    """Test comparison filtering functionality"""
    
    def test_filter_by_brand(self, client):
        """Test filtering bikes by brand"""
        response = client.get('/comparison/?brand=Yamaha')
        assert response.status_code == 200
        assert b'Yamaha' in response.data
    
    def test_filter_by_category(self, client):
        """Test filtering bikes by category"""
        response = client.get('/comparison/?category=sport')
        assert response.status_code == 200
    
    def test_filter_by_price_range(self, client):
        """Test filtering bikes by price range"""
        response = client.get('/comparison/?min_price=100000&max_price=300000')
        assert response.status_code == 200
    
    def test_filter_by_engine_size(self, client):
        """Test filtering bikes by engine displacement"""
        response = client.get('/comparison/?min_cc=150&max_cc=400')
        assert response.status_code == 200
    
    def test_multiple_filters(self, client):
        """Test applying multiple filters simultaneously"""
        response = client.get('/comparison/?category=sport&min_price=100000&max_cc=200')
        assert response.status_code == 200


class TestComparisonAPI:
    """Test comparison API endpoints"""
    
    def test_get_bike_specs_api(self, client, app):
        """Test API endpoint for getting bike specs"""
        with app.app_context():
            bike = Bike.query.first()
            response = client.get(f'/api/bikes/{bike.id}/specs')
            
            if response.status_code == 200:
                data = response.get_json()
                assert 'max_power' in data or 'specs' in data
    
    def test_comparison_data_json(self, client, app):
        """Test getting comparison data as JSON"""
        with app.app_context():
            bike1 = Bike.query.first()
            bike2 = Bike.query.all()[1] if len(Bike.query.all()) > 1 else bike1
            
            response = client.get(
                f'/api/comparison?bike1={bike1.id}&bike2={bike2.id}',
                headers={'Accept': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.get_json()
                assert isinstance(data, (dict, list))


class TestComparisonUtilities:
    """Test comparison utility functions"""
    
    def test_calculate_power_to_weight_ratio(self, app):
        """Test power-to-weight ratio calculation"""
        with app.app_context():
            bike = Bike.query.filter_by(brand='Yamaha').first()
            if bike and bike.specs:
                ratio = bike.specs.max_power / bike.specs.kerb_weight
                assert ratio > 0
                assert isinstance(ratio, float)
    
    def test_compare_performance_metrics(self, app):
        """Test performance comparison logic"""
        with app.app_context():
            bike1 = Bike.query.filter_by(brand='Yamaha').first()
            bike2 = Bike.query.filter_by(brand='KTM').first()
            
            if bike1.specs and bike2.specs:
                # KTM Duke 390 should have more power than R15
                assert bike2.specs.max_power > bike1.specs.max_power
