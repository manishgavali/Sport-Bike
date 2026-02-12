from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user_bikes import UserBike
from app.models.ride_logs import RideLog
from app.models.maintenance_records import MaintenanceRecord
from app.models.bike import Bike
from app import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import json

dashboard_bp = Blueprint('dashboard', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dashboard_bp.route('/')
@login_required
def index():
    # Get user's bikes
    user_bikes = UserBike.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    # Get total stats
    total_bikes = len(user_bikes)
    total_rides = RideLog.query.join(UserBike).filter(UserBike.user_id == current_user.id).count()
    total_maintenance = MaintenanceRecord.query.join(UserBike).filter(UserBike.user_id == current_user.id).count()
    
    # Calculate total distance
    total_distance = db.session.query(db.func.sum(RideLog.distance)).join(UserBike).filter(
        UserBike.user_id == current_user.id
    ).scalar() or 0
    
    return render_template('dashboard/index.html',
                         user_bikes=user_bikes,
                         total_bikes=total_bikes,
                         total_rides=total_rides,
                         total_maintenance=total_maintenance,
                         total_distance=round(total_distance, 2))

@dashboard_bp.route('/my-bikes')
@login_required
def my_bikes():
    user_bikes = UserBike.query.filter_by(user_id=current_user.id, is_active=True).all()
    all_bikes = Bike.query.filter_by(is_active=True).order_by(Bike.brand, Bike.model).all()
    return render_template('dashboard/my_bikes.html', user_bikes=user_bikes, all_bikes=all_bikes)

@dashboard_bp.route('/add-bike', methods=['POST'])
@login_required
def add_bike():
    try:
        bike_id = request.form.get('bike_id', type=int)
        registration_number = request.form.get('registration_number', '').strip()
        purchase_date = request.form.get('purchase_date')
        purchase_price = request.form.get('purchase_price', type=float)
        current_km = request.form.get('current_km', type=int, default=0)
        bike_condition = request.form.get('bike_condition', 'good')
        
        # Validate bike exists
        bike = Bike.query.get(bike_id)
        if not bike:
            flash('Invalid bike selected', 'error')
            return redirect(url_for('dashboard.my_bikes'))
        
        # Check if already added
        if registration_number:
            existing = UserBike.query.filter_by(
                user_id=current_user.id,
                registration_number=registration_number
            ).first()
            
            if existing:
                flash('This registration number is already in your garage', 'warning')
                return redirect(url_for('dashboard.my_bikes'))
        
        # Parse date
        purchase_date_obj = None
        if purchase_date:
            purchase_date_obj = datetime.strptime(purchase_date, '%Y-%m-%d')
        
        # Handle image upload
        bike_images_list = []
        if 'bike_images' in request.files:
            files = request.files.getlist('bike_images')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to make unique
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    
                    # Create upload directory if it doesn't exist
                    upload_folder = os.path.join('app', 'static', 'uploads', 'bikes')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Save file
                    filepath = os.path.join(upload_folder, filename)
                    file.save(filepath)
                    
                    # Store relative path for web access
                    bike_images_list.append(f'/static/uploads/bikes/{filename}')
        
        # Create user bike
        user_bike = UserBike(
            user_id=current_user.id,
            bike_id=bike_id,
            registration_number=registration_number or None,
            purchase_date=purchase_date_obj,
            purchase_price=purchase_price,
            current_km=current_km,
            bike_condition=bike_condition,
            bike_images=json.dumps(bike_images_list) if bike_images_list else None,
            is_active=True
        )
        
        db.session.add(user_bike)
        db.session.commit()
        
        flash(f'{bike.brand} {bike.model} added to your garage successfully! 🏍️', 'success')
        return redirect(url_for('dashboard.my_bikes'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding bike: {str(e)}', 'error')
        return redirect(url_for('dashboard.my_bikes'))

@dashboard_bp.route('/bike-details/<int:bike_id>')
@login_required
def bike_details(bike_id):
    user_bike = UserBike.query.filter_by(id=bike_id, user_id=current_user.id).first_or_404()
    
    # Parse images
    images = []
    if user_bike.bike_images:
        try:
            images = json.loads(user_bike.bike_images)
        except:
            images = []
    
    return render_template('dashboard/bike_details.html', user_bike=user_bike, images=images)

@dashboard_bp.route('/analytics')
@login_required
def analytics():
    # Get all user bikes
    user_bikes = UserBike.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    # Get all ride logs for user
    ride_logs = RideLog.query.join(UserBike).filter(
        UserBike.user_id == current_user.id
    ).order_by(RideLog.ride_date.desc()).all()
    
    # Calculate statistics
    total_distance = sum([log.distance for log in ride_logs if log.distance])
    total_fuel = sum([log.fuel_consumed for log in ride_logs if log.fuel_consumed])
    avg_speed = sum([log.avg_speed for log in ride_logs if log.avg_speed]) / len(ride_logs) if ride_logs else 0
    
    # Prepare chart data
    chart_data = {
        'dates': [log.ride_date.strftime('%Y-%m-%d') for log in ride_logs[-10:]],
        'distances': [log.distance for log in ride_logs[-10:]],
        'speeds': [log.avg_speed for log in ride_logs[-10:]],
        'fuel': [log.fuel_consumed for log in ride_logs[-10:]]
    }
    
    return render_template('dashboard/analytics.html',
                         user_bikes=user_bikes,
                         ride_logs=ride_logs[:10],
                         total_distance=round(total_distance, 2),
                         total_fuel=round(total_fuel, 2),
                         avg_speed=round(avg_speed, 2),
                         chart_data=chart_data)

@dashboard_bp.route('/add-ride-log/<int:bike_id>', methods=['GET', 'POST'])
@login_required
def add_ride_log(bike_id):
    user_bike = UserBike.query.filter_by(id=bike_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        try:
            ride_log = RideLog(
                user_bike_id=bike_id,
                ride_date=datetime.strptime(request.form.get('ride_date'), '%Y-%m-%d') if request.form.get('ride_date') else datetime.utcnow(),
                distance=request.form.get('distance', type=float),
                duration=request.form.get('duration', type=int),
                avg_speed=request.form.get('avg_speed', type=float),
                max_speed=request.form.get('max_speed', type=float),
                fuel_consumed=request.form.get('fuel_consumed', type=float),
                road_type=request.form.get('road_type'),
                weather_condition=request.form.get('weather_condition'),
                riding_style=request.form.get('riding_style'),
                start_location=request.form.get('start_location'),
                end_location=request.form.get('end_location'),
                notes=request.form.get('notes')
            )
            
            # Update bike's current KM
            if ride_log.distance:
                user_bike.current_km += int(ride_log.distance)
            
            db.session.add(ride_log)
            db.session.commit()
            
            flash('Ride log added successfully!', 'success')
            return redirect(url_for('dashboard.bike_details', bike_id=bike_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding ride log: {str(e)}', 'error')
    
    return render_template('dashboard/add_ride_log.html', user_bike=user_bike)

@dashboard_bp.route('/bike-performance/<int:bike_id>')
@login_required
def bike_performance(bike_id):
    user_bike = UserBike.query.filter_by(id=bike_id, user_id=current_user.id).first_or_404()
    
    # Get recent ride logs for this bike
    ride_logs = RideLog.query.filter_by(user_bike_id=bike_id).order_by(
        RideLog.ride_date.desc()
    ).limit(20).all()
    
    # Calculate performance metrics
    if ride_logs:
        total_distance = sum([log.distance for log in ride_logs if log.distance])
        total_fuel = sum([log.fuel_consumed for log in ride_logs if log.fuel_consumed])
        avg_speed = sum([log.avg_speed for log in ride_logs if log.avg_speed]) / len([log for log in ride_logs if log.avg_speed])
        avg_mileage = (total_distance / total_fuel) if total_fuel > 0 else 0
        
        # Calculate health score (0-100)
        # Based on: regular maintenance, smooth riding, good mileage
        health_score = 85  # Base score
        
        # Reduce if aggressive riding
        aggressive_rides = len([log for log in ride_logs if log.riding_style == 'aggressive'])
        health_score -= (aggressive_rides / len(ride_logs)) * 15
        
        # Check maintenance regularity
        recent_maintenance = MaintenanceRecord.query.filter_by(
            user_bike_id=bike_id
        ).order_by(MaintenanceRecord.service_date.desc()).first()
        
        if not recent_maintenance:
            health_score -= 10
        
        # Heat level estimation (based on riding style and usage)
        heat_level = 'Normal'
        if aggressive_rides > len(ride_logs) * 0.5:
            heat_level = 'High'
        elif aggressive_rides > len(ride_logs) * 0.3:
            heat_level = 'Medium'
        
        performance_data = {
            'avg_speed': round(avg_speed, 2),
            'avg_mileage': round(avg_mileage, 2),
            'total_distance': round(total_distance, 2),
            'total_fuel': round(total_fuel, 2),
            'health_score': round(health_score, 1),
            'heat_level': heat_level,
            'total_rides': len(ride_logs)
        }
    else:
        performance_data = {
            'avg_speed': 0,
            'avg_mileage': 0,
            'total_distance': 0,
            'total_fuel': 0,
            'health_score': 100,
            'heat_level': 'Normal',
            'total_rides': 0
        }
    
    return render_template('dashboard/bike_performance.html',
                         user_bike=user_bike,
                         performance=performance_data,
                         ride_logs=ride_logs[:10])
