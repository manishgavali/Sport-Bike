from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.bike import Bike
from app.models.user_bikes import UserBike
from app.services.safety_advisor import SafetyAdvisor

safety_bp = Blueprint('safety', __name__)

@safety_bp.route('/')
@login_required
def index():
    user_bikes = UserBike.query.filter_by(user_id=current_user.id, is_active=True).all()
    return render_template('safety/tips.html', user_bikes=user_bikes)

@safety_bp.route('/tips/<int:bike_id>')
@login_required
def get_tips(bike_id):
    user_bike = UserBike.query.filter_by(id=bike_id, user_id=current_user.id).first_or_404()
    
    # Get AI safety recommendations
    advisor = SafetyAdvisor()
    tips = advisor.generate_safety_tips(
        bike=user_bike.bike,
        rider_experience=current_user.riding_experience,
        bike_condition=user_bike.bike_condition
    )
    
    return jsonify(tips)

@safety_bp.route('/alerts')
@login_required
def alerts():
    user_bikes = UserBike.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    # Generate alerts for all bikes
    advisor = SafetyAdvisor()
    all_alerts = []
    
    for user_bike in user_bikes:
        alerts = advisor.check_safety_alerts(user_bike)
        if alerts:
            all_alerts.extend(alerts)
    
    return render_template('safety/alerts.html', alerts=all_alerts)
