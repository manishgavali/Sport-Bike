from flask import Blueprint, render_template, request, jsonify
from app.models.bike import Bike
from app.services.cost_calculator import CostCalculator

calculator_bp = Blueprint('calculator', __name__)

@calculator_bp.route('/')
def index():
    bikes = Bike.query.filter_by(is_active=True).all()
    return render_template('calculator/ownership_cost.html', bikes=bikes)

@calculator_bp.route('/calculate', methods=['POST'])
def calculate():
    bike_id = request.form.get('bike_id', type=int)
    yearly_km = request.form.get('yearly_km', type=float)
    fuel_price = request.form.get('fuel_price', type=float)
    insurance_type = request.form.get('insurance_type')
    
    bike = Bike.query.get_or_404(bike_id)
    calculator = CostCalculator()
    
    results = calculator.calculate_ownership_cost(
        bike=bike,
        yearly_km=yearly_km,
        fuel_price=fuel_price,
        insurance_type=insurance_type
    )
    
    return jsonify(results)
