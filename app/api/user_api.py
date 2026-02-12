from flask import jsonify, request
from flask_login import login_required, current_user
from app.api import api_bp
from app.models.user import User
from app.models.user_bikes import UserBike
from app.models.ride_logs import RideLog
from app.models.maintenance_records import MaintenanceRecord
from app.models.reviews import Review
from app import db
from functools import wraps

def token_required(f):
    """Decorator for API token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Token is missing'
            }), 401
        
        # In production, implement proper JWT token verification
        # For now, we'll use session-based auth with login_required
        
        return f(*args, **kwargs)
    
    return decorated


@api_bp.route('/user/profile', methods=['GET'])
@login_required
def get_user_profile():
    """Get current user profile"""
    try:
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'full_name': current_user.full_name,
            'phone': current_user.phone,
            'riding_experience': current_user.riding_experience,
            'profile_image': current_user.profile_image,
            'role': current_user.role,
            'created_at': current_user.created_at.strftime('%Y-%m-%d'),
            'is_active': current_user.is_active
        }
        
        return jsonify({
            'success': True,
            'data': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/user/bikes', methods=['GET'])
@login_required
def get_user_bikes():
    """Get all bikes owned by current user"""
    try:
        user_bikes = UserBike.query.filter_by(
            user_id=current_user.id, 
            is_active=True
        ).all()
        
        bikes_data = []
        for user_bike in user_bikes:
            bikes_data.append({
                'id': user_bike.id,
                'bike': {
                    'id': user_bike.bike.id,
                    'brand': user_bike.bike.brand,
                    'model': user_bike.bike.model,
                    'year': user_bike.bike.year
                },
                'registration_number': user_bike.registration_number,
                'purchase_date': user_bike.purchase_date.strftime('%Y-%m-%d') if user_bike.purchase_date else None,
                'purchase_price': user_bike.purchase_price,
                'current_km': user_bike.current_km,
                'condition': user_bike.bike_condition,
                'modifications': user_bike.modifications
            })
        
        return jsonify({
            'success': True,
            'count': len(bikes_data),
            'data': bikes_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/user/bikes/<int:user_bike_id>', methods=['GET'])
@login_required
def get_user_bike_details(user_bike_id):
    """Get detailed information about user's bike"""
    try:
        user_bike = UserBike.query.filter_by(
            id=user_bike_id, 
            user_id=current_user.id
        ).first_or_404()
        
        # Get ride statistics
        total_rides = RideLog.query.filter_by(user_bike_id=user_bike_id).count()
        total_distance = db.session.query(
            db.func.sum(RideLog.distance)
        ).filter_by(user_bike_id=user_bike_id).scalar() or 0
        
        # Get maintenance count
        maintenance_count = MaintenanceRecord.query.filter_by(
            user_bike_id=user_bike_id
        ).count()
        
        bike_data = {
            'id': user_bike.id,
            'bike': {
                'id': user_bike.bike.id,
                'brand': user_bike.bike.brand,
                'model': user_bike.bike.model,
                'year': user_bike.bike.year,
                'category': user_bike.bike.category
            },
            'registration_number': user_bike.registration_number,
            'purchase_date': user_bike.purchase_date.strftime('%Y-%m-%d') if user_bike.purchase_date else None,
            'purchase_price': user_bike.purchase_price,
            'current_km': user_bike.current_km,
            'condition': user_bike.bike_condition,
            'modifications': user_bike.modifications,
            'statistics': {
                'total_rides': total_rides,
                'total_distance': round(total_distance, 2),
                'maintenance_records': maintenance_count
            }
        }
        
        return jsonify({
            'success': True,
            'data': bike_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@api_bp.route('/user/rides', methods=['GET'])
@login_required
def get_user_rides():
    """Get ride logs for user's bikes"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        bike_id = request.args.get('bike_id', type=int)
        
        # Build query
        query = RideLog.query.join(UserBike).filter(
            UserBike.user_id == current_user.id
        )
        
        if bike_id:
            query = query.filter(RideLog.user_bike_id == bike_id)
        
        total_count = query.count()
        rides = query.order_by(RideLog.ride_date.desc()).limit(limit).offset(offset).all()
        
        rides_data = []
        for ride in rides:
            rides_data.append({
                'id': ride.id,
                'bike': {
                    'brand': ride.user_bike.bike.brand,
                    'model': ride.user_bike.bike.model
                },
                'ride_date': ride.ride_date.strftime('%Y-%m-%d %H:%M'),
                'distance': ride.distance,
                'duration': ride.duration,
                'avg_speed': ride.avg_speed,
                'max_speed': ride.max_speed,
                'fuel_consumed': ride.fuel_consumed,
                'road_type': ride.road_type,
                'weather_condition': ride.weather_condition,
                'riding_style': ride.riding_style,
                'start_location': ride.start_location,
                'end_location': ride.end_location
            })
        
        return jsonify({
            'success': True,
            'total_count': total_count,
            'returned_count': len(rides_data),
            'data': rides_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/user/maintenance', methods=['GET'])
@login_required
def get_user_maintenance():
    """Get maintenance records for user's bikes"""
    try:
        limit = request.args.get('limit', 50, type=int)
        bike_id = request.args.get('bike_id', type=int)
        
        query = MaintenanceRecord.query.join(UserBike).filter(
            UserBike.user_id == current_user.id
        )
        
        if bike_id:
            query = query.filter(MaintenanceRecord.user_bike_id == bike_id)
        
        records = query.order_by(
            MaintenanceRecord.service_date.desc()
        ).limit(limit).all()
        
        records_data = []
        for record in records:
            records_data.append({
                'id': record.id,
                'bike': {
                    'brand': record.user_bike.bike.brand,
                    'model': record.user_bike.bike.model
                },
                'maintenance_type': record.maintenance_type,
                'service_date': record.service_date.strftime('%Y-%m-%d'),
                'odometer_reading': record.odometer_reading,
                'description': record.description,
                'parts_replaced': record.parts_replaced,
                'cost': record.cost,
                'service_center': record.service_center
            })
        
        return jsonify({
            'success': True,
            'count': len(records_data),
            'data': records_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/user/reviews', methods=['GET'])
@login_required
def get_user_reviews():
    """Get reviews written by current user"""
    try:
        reviews = Review.query.filter_by(
            user_id=current_user.id
        ).order_by(Review.created_at.desc()).all()
        
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                'id': review.id,
                'bike': {
                    'id': review.bike.id,
                    'brand': review.bike.brand,
                    'model': review.bike.model
                },
                'rating': review.rating,
                'title': review.title,
                'content': review.content,
                'performance_rating': review.performance_rating,
                'comfort_rating': review.comfort_rating,
                'mileage_rating': review.mileage_rating,
                'looks_rating': review.looks_rating,
                'ownership_duration': review.ownership_duration,
                'km_driven': review.km_driven,
                'pros': review.pros,
                'cons': review.cons,
                'is_verified': review.is_verified,
                'likes_count': review.likes_count,
                'created_at': review.created_at.strftime('%Y-%m-%d')
            })
        
        return jsonify({
            'success': True,
            'count': len(reviews_data),
            'data': reviews_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/user/stats', methods=['GET'])
@login_required
def get_user_stats():
    """Get user statistics"""
    try:
        # Get bike count
        bike_count = UserBike.query.filter_by(
            user_id=current_user.id, 
            is_active=True
        ).count()
        
        # Get total rides
        total_rides = db.session.query(db.func.count(RideLog.id)).join(
            UserBike
        ).filter(UserBike.user_id == current_user.id).scalar() or 0
        
        # Get total distance
        total_distance = db.session.query(db.func.sum(RideLog.distance)).join(
            UserBike
        ).filter(UserBike.user_id == current_user.id).scalar() or 0
        
        # Get maintenance count
        maintenance_count = db.session.query(
            db.func.count(MaintenanceRecord.id)
        ).join(UserBike).filter(UserBike.user_id == current_user.id).scalar() or 0
        
        # Get review count
        review_count = Review.query.filter_by(user_id=current_user.id).count()
        
        stats = {
            'bikes_owned': bike_count,
            'total_rides': total_rides,
            'total_distance_km': round(total_distance, 2),
            'maintenance_records': maintenance_count,
            'reviews_written': review_count
        }
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
