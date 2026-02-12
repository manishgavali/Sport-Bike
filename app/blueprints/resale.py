from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app.models.bike import Bike
from app.models.user_bikes import UserBike
from app.services.resale_predictor import ResalePredictor

resale_bp = Blueprint('resale', __name__)

@resale_bp.route('/')
def index():
    all_bikes = Bike.query.filter_by(is_active=True).all()
    user_bikes = None
    if current_user.is_authenticated:
        user_bikes = UserBike.query.filter_by(user_id=current_user.id).all()
    return render_template('resale/prediction.html', all_bikes=all_bikes, user_bikes=user_bikes)

@resale_bp.route('/predict', methods=['POST'])
def predict():
    bike_id = request.form.get('bike_id', type=int)
    purchase_price = request.form.get('purchase_price', type=float)
    years_old = request.form.get('years_old', type=int)
    km_driven = request.form.get('km_driven', type=int)
    condition = request.form.get('condition')
    
    bike = Bike.query.get_or_404(bike_id)
    predictor = ResalePredictor()
    
    prediction = predictor.predict_resale_value(
        bike=bike,
        purchase_price=purchase_price,
        years_old=years_old,
        km_driven=km_driven,
        condition=condition
    )
    
    return jsonify(prediction)
