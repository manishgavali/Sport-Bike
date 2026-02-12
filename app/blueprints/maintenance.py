from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user_bikes import UserBike
from app.models.maintenance_records import MaintenanceRecord
from app.services.maintenance_predictor import MaintenancePredictor
from datetime import datetime

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/')
@login_required
def index():
    user_bikes = UserBike.query.filter_by(user_id=current_user.id, is_active=True).all()
    return render_template('maintenance/dashboard.html', user_bikes=user_bikes)

@maintenance_bp.route('/schedule/<int:bike_id>')
@login_required
def schedule(bike_id):
    user_bike = UserBike.query.filter_by(id=bike_id, user_id=current_user.id).first_or_404()
    
    # Get maintenance predictions
    predictor = MaintenancePredictor()
    predictions = predictor.predict_maintenance(user_bike)
    
    return render_template('maintenance/schedule.html', 
                         user_bike=user_bike, 
                         predictions=predictions)

@maintenance_bp.route('/history/<int:bike_id>')
@login_required
def history(bike_id):
    user_bike = UserBike.query.filter_by(id=bike_id, user_id=current_user.id).first_or_404()
    records = MaintenanceRecord.query.filter_by(user_bike_id=bike_id).order_by(
        MaintenanceRecord.service_date.desc()
    ).all()
    
    return render_template('maintenance/history.html', 
                         user_bike=user_bike, 
                         records=records)

@maintenance_bp.route('/add-record/<int:bike_id>', methods=['POST'])
@login_required
def add_record(bike_id):
    user_bike = UserBike.query.filter_by(id=bike_id, user_id=current_user.id).first_or_404()
    
    record = MaintenanceRecord(
        user_bike_id=bike_id,
        maintenance_type=request.form.get('maintenance_type'),
        service_date=datetime.strptime(request.form.get('service_date'), '%Y-%m-%d').date(),
        odometer_reading=request.form.get('odometer_reading', type=int),
        description=request.form.get('description'),
        parts_replaced=request.form.get('parts_replaced'),
        cost=request.form.get('cost', type=float),
        service_center=request.form.get('service_center')
    )
    
    db.session.add(record)
    db.session.commit()
    
    flash('Maintenance record added successfully!', 'success')
    return redirect(url_for('maintenance.history', bike_id=bike_id))
