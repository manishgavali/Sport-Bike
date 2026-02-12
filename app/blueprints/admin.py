from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.bike import Bike
from app.models.bike_specs import BikeSpec
from app.models.reviews import Review
from app.models.admin_logs import AdminLog
from app.models.accident_reports import AccidentReport
from app.models.user_bikes import UserBike
from app.models.ride_logs import RideLog
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    total_users = User.query.count()
    total_bikes = Bike.query.count()
    pending_reviews = Review.query.filter_by(is_verified=False).count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_bikes=total_bikes,
                         pending_reviews=pending_reviews)

@admin_bp.route('/manage-bikes')
@login_required
@admin_required
def manage_bikes():
    bikes = Bike.query.all()
    return render_template('admin/manage_bikes.html', bikes=bikes)

@admin_bp.route('/manage-users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    # Get comprehensive analytics
    
    # User statistics
    total_users = User.query.count()
    new_users_this_month = User.query.filter(
        User.created_at >= datetime.utcnow() - timedelta(days=30)
    ).count()
    
    # Bike statistics
    total_bikes = Bike.query.count()
    total_user_bikes = UserBike.query.count()
    
    # Popular bikes (most owned)
    popular_bikes = db.session.query(
        Bike.brand, Bike.model, func.count(UserBike.id).label('count')
    ).join(UserBike).group_by(Bike.id).order_by(
        func.count(UserBike.id).desc()
    ).limit(10).all()
    
    # Most reviewed bikes
    most_reviewed = db.session.query(
        Bike.brand, Bike.model, func.count(Review.id).label('review_count')
    ).join(Review).group_by(Bike.id).order_by(
        func.count(Review.id).desc()
    ).limit(10).all()
    
    # Accident statistics
    total_accidents = AccidentReport.query.count()
    accidents_by_severity = db.session.query(
        AccidentReport.severity, func.count(AccidentReport.id).label('count')
    ).group_by(AccidentReport.severity).all()
    
    # Bike problems trends (from accident reports)
    problem_trends = db.session.query(
        AccidentReport.incident_type, func.count(AccidentReport.id).label('count')
    ).group_by(AccidentReport.incident_type).order_by(
        func.count(AccidentReport.id).desc()
    ).limit(10).all()
    
    # User activity
    total_rides = RideLog.query.count()
    rides_this_month = RideLog.query.filter(
        RideLog.ride_date >= datetime.utcnow() - timedelta(days=30)
    ).count()
    
    # Review statistics
    total_reviews = Review.query.count()
    pending_reviews = Review.query.filter_by(is_verified=False).count()
    
    return render_template('admin/analytics.html',
                         total_users=total_users,
                         new_users_this_month=new_users_this_month,
                         total_bikes=total_bikes,
                         total_user_bikes=total_user_bikes,
                         popular_bikes=popular_bikes,
                         most_reviewed=most_reviewed,
                         total_accidents=total_accidents,
                         accidents_by_severity=accidents_by_severity,
                         problem_trends=problem_trends,
                         total_rides=total_rides,
                         rides_this_month=rides_this_month,
                         total_reviews=total_reviews,
                         pending_reviews=pending_reviews)

@admin_bp.route('/add-bike', methods=['GET', 'POST'])
@login_required
@admin_required
def add_bike():
    if request.method == 'POST':
        try:
            bike = Bike(
                brand=request.form.get('brand'),
                model=request.form.get('model'),
                year=request.form.get('year', type=int),
                category=request.form.get('category'),
                price=request.form.get('price', type=float),
                image_url=request.form.get('image_url'),
                is_active=True
            )
            
            db.session.add(bike)
            db.session.flush()  # Get the bike ID
            
            # Add specifications if provided
            if request.form.get('engine_cc'):
                specs = BikeSpec(
                    bike_id=bike.id,
                    engine_cc=request.form.get('engine_cc', type=int),
                    engine_type=request.form.get('engine_type'),
                    max_power=request.form.get('max_power', type=float),
                    max_torque=request.form.get('max_torque', type=float),
                    top_speed=request.form.get('top_speed', type=int),
                    mileage=request.form.get('mileage', type=int),
                    fuel_capacity=request.form.get('fuel_capacity', type=float),
                    weight=request.form.get('weight', type=int),
                    seat_height=request.form.get('seat_height', type=int)
                )
                db.session.add(specs)
            
            db.session.commit()
            
            # Log action
            log = AdminLog(
                admin_id=current_user.id,
                action='add_bike',
                description=f'Added bike: {bike.brand} {bike.model}'
            )
            db.session.add(log)
            db.session.commit()
            
            flash(f'Bike {bike.brand} {bike.model} added successfully!', 'success')
            return redirect(url_for('admin.manage_bikes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding bike: {str(e)}', 'error')
    
    return render_template('admin/add_bike.html')

@admin_bp.route('/edit-bike/<int:bike_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_bike(bike_id):
    bike = Bike.query.get_or_404(bike_id)
    
    if request.method == 'POST':
        try:
            bike.brand = request.form.get('brand')
            bike.model = request.form.get('model')
            bike.year = request.form.get('year', type=int)
            bike.category = request.form.get('category')
            bike.price = request.form.get('price', type=float)
            bike.image_url = request.form.get('image_url')
            bike.is_active = request.form.get('is_active') == 'on'
            
            # Update specifications
            if bike.specs:
                bike.specs.engine_cc = request.form.get('engine_cc', type=int)
                bike.specs.engine_type = request.form.get('engine_type')
                bike.specs.max_power = request.form.get('max_power', type=float)
                bike.specs.max_torque = request.form.get('max_torque', type=float)
                bike.specs.top_speed = request.form.get('top_speed', type=int)
                bike.specs.mileage = request.form.get('mileage', type=int)
                bike.specs.fuel_capacity = request.form.get('fuel_capacity', type=float)
                bike.specs.weight = request.form.get('weight', type=int)
                bike.specs.seat_height = request.form.get('seat_height', type=int)
            elif request.form.get('engine_cc'):
                specs = BikeSpec(
                    bike_id=bike.id,
                    engine_cc=request.form.get('engine_cc', type=int),
                    engine_type=request.form.get('engine_type'),
                    max_power=request.form.get('max_power', type=float),
                    max_torque=request.form.get('max_torque', type=float),
                    top_speed=request.form.get('top_speed', type=int),
                    mileage=request.form.get('mileage', type=int),
                    fuel_capacity=request.form.get('fuel_capacity', type=float),
                    weight=request.form.get('weight', type=int),
                    seat_height=request.form.get('seat_height', type=int)
                )
                db.session.add(specs)
            
            db.session.commit()
            
            # Log action
            log = AdminLog(
                admin_id=current_user.id,
                action='edit_bike',
                description=f'Updated bike: {bike.brand} {bike.model}'
            )
            db.session.add(log)
            db.session.commit()
            
            flash(f'Bike {bike.brand} {bike.model} updated successfully!', 'success')
            return redirect(url_for('admin.manage_bikes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating bike: {str(e)}', 'error')
    
    return render_template('admin/edit_bike.html', bike=bike)

@admin_bp.route('/delete-bike/<int:bike_id>', methods=['POST'])
@login_required
@admin_required
def delete_bike(bike_id):
    bike = Bike.query.get_or_404(bike_id)
    
    try:
        # Soft delete - just mark as inactive
        bike.is_active = False
        db.session.commit()
        
        # Log action
        log = AdminLog(
            admin_id=current_user.id,
            action='delete_bike',
            description=f'Deactivated bike: {bike.brand} {bike.model}'
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Bike {bike.brand} {bike.model} deactivated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deactivating bike: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_bikes'))

@admin_bp.route('/toggle-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot deactivate your own account!', 'error')
        return redirect(url_for('admin.manage_users'))
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        
        status = 'activated' if user.is_active else 'deactivated'
        
        # Log action
        log = AdminLog(
            admin_id=current_user.id,
            action='toggle_user',
            description=f'{status.capitalize()} user: {user.username}'
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'User {user.username} {status} successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error toggling user status: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/view-accidents')
@login_required
@admin_required
def view_accidents():
    # Get all accident reports with statistics
    accidents = AccidentReport.query.order_by(
        AccidentReport.incident_date.desc()
    ).all()
    
    # Group by bike to show problem patterns
    bike_problems = db.session.query(
        Bike.brand, Bike.model,
        func.count(AccidentReport.id).label('incident_count'),
        AccidentReport.incident_type
    ).join(Bike).group_by(
        Bike.id, AccidentReport.incident_type
    ).order_by(
        func.count(AccidentReport.id).desc()
    ).limit(20).all()
    
    return render_template('admin/view_accidents.html',
                         accidents=accidents,
                         bike_problems=bike_problems)
