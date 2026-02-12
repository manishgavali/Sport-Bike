from flask import Blueprint, render_template, request, jsonify
from app.models.bike import Bike
from app.services.performance_simulator import PerformanceSimulator

simulator_bp = Blueprint('simulator', __name__)

@simulator_bp.route('/')
def index():
    from flask_login import current_user
    from app.models.user_bikes import UserBike
    
    # Get all active bikes
    all_bikes = Bike.query.filter_by(is_active=True).order_by(Bike.brand, Bike.model).all()
    
    # Get user's bikes if logged in
    user_bikes = []
    if current_user.is_authenticated:
        user_bikes = UserBike.query.filter_by(user_id=current_user.id).all()
    
    return render_template('simulator/input_form.html', all_bikes=all_bikes, user_bikes=user_bikes)

@simulator_bp.route('/simulate', methods=['POST'])
def simulate():
    bike_id = request.form.get('bike_id')
    rider_weight = float(request.form.get('rider_weight', 70))
    road_type = request.form.get('road_type', 'city')
    weather = request.form.get('weather', 'sunny')
    riding_style = request.form.get('riding_style', 'moderate')
    
    bike = Bike.query.get_or_404(bike_id)
    simulator = PerformanceSimulator()
    
    results = simulator.simulate_performance(
        bike=bike,
        rider_weight=rider_weight,
        road_type=road_type,
        weather=weather,
        riding_style=riding_style
    )
    
    return render_template('simulator/results.html', bike=bike, results=results)
