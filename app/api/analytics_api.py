from flask import jsonify, request
from flask_login import login_required, current_user
from app.api import api_bp
from app.models.bike import Bike
from app.models.user import User
from app.models.reviews import Review
from app.models.accident_reports import AccidentReport
from app.models.ride_logs import RideLog
from app.models.user_bikes import UserBike
from app import db
from sqlalchemy import func, extract
from datetime import datetime, timedelta

@api_bp.route('/analytics/overview', methods=['GET'])
def get_platform_overview():
    """Get platform-wide analytics overview"""
    try:
        # Total counts
        total_bikes = Bike.query.filter_by(is_active=True).count()
        total_users = User.query.filter_by(is_active=True).count()
        total_reviews = Review.query.filter_by(is_verified=True).count()
        total_rides = RideLog.query.count()
        
        # Calculate total distance
        total_distance = db.session.query(
            func.sum(RideLog.distance)
        ).scalar() or 0
        
        overview = {
            'total_bikes': total_bikes,
            'total_users': total_users,
            'total_reviews': total_reviews,
            'total_rides': total_rides,
            'total_distance_km': round(total_distance, 2)
        }
        
        return jsonify({
            'success': True,
            'data': overview
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/popular-bikes', methods=['GET'])
def get_popular_bikes():
    """Get most popular bikes based on reviews and ownership"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Get bikes with most reviews
        popular = db.session.query(
            Bike,
            func.count(Review.id).label('review_count'),
            func.avg(Review.rating).label('avg_rating')
        ).join(Review).filter(
            Bike.is_active == True,
            Review.is_verified == True
        ).group_by(Bike.id).order_by(
            func.count(Review.id).desc()
        ).limit(limit).all()
        
        popular_bikes = []
        for bike, review_count, avg_rating in popular:
            popular_bikes.append({
                'bike': {
                    'id': bike.id,
                    'brand': bike.brand,
                    'model': bike.model,
                    'year': bike.year,
                    'price': bike.price,
                    'category': bike.category
                },
                'review_count': review_count,
                'average_rating': round(avg_rating, 2)
            })
        
        return jsonify({
            'success': True,
            'data': popular_bikes
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/top-rated', methods=['GET'])
def get_top_rated_bikes():
    """Get highest rated bikes"""
    try:
        limit = request.args.get('limit', 10, type=int)
        min_reviews = request.args.get('min_reviews', 5, type=int)
        
        top_rated = db.session.query(
            Bike,
            func.avg(Review.rating).label('avg_rating'),
            func.count(Review.id).label('review_count')
        ).join(Review).filter(
            Bike.is_active == True,
            Review.is_verified == True
        ).group_by(Bike.id).having(
            func.count(Review.id) >= min_reviews
        ).order_by(
            func.avg(Review.rating).desc()
        ).limit(limit).all()
        
        top_bikes = []
        for bike, avg_rating, review_count in top_rated:
            top_bikes.append({
                'bike': {
                    'id': bike.id,
                    'brand': bike.brand,
                    'model': bike.model,
                    'year': bike.year,
                    'price': bike.price
                },
                'average_rating': round(avg_rating, 2),
                'review_count': review_count
            })
        
        return jsonify({
            'success': True,
            'data': top_bikes
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/safety-reports', methods=['GET'])
def get_safety_reports():
    """Get accident and safety statistics"""
    try:
        # Get reports by severity
        severity_stats = db.session.query(
            AccidentReport.severity,
            func.count(AccidentReport.id).label('count')
        ).group_by(AccidentReport.severity).all()
        
        # Get reports by incident type
        type_stats = db.session.query(
            AccidentReport.incident_type,
            func.count(AccidentReport.id).label('count')
        ).group_by(AccidentReport.incident_type).all()
        
        # Get most reported bikes
        bike_reports = db.session.query(
            Bike.brand,
            Bike.model,
            func.count(AccidentReport.id).label('report_count')
        ).join(AccidentReport).group_by(
            Bike.id
        ).order_by(
            func.count(AccidentReport.id).desc()
        ).limit(10).all()
        
        safety_data = {
            'by_severity': [
                {'severity': sev, 'count': count} 
                for sev, count in severity_stats
            ],
            'by_type': [
                {'type': type_, 'count': count} 
                for type_, count in type_stats
            ],
            'most_reported_bikes': [
                {
                    'bike': f"{brand} {model}",
                    'report_count': count
                }
                for brand, model, count in bike_reports
            ]
        }
        
        return jsonify({
            'success': True,
            'data': safety_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/riding-patterns', methods=['GET'])
@login_required
def get_riding_patterns():
    """Get user's riding pattern analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        # Get rides in date range
        rides = db.session.query(RideLog).join(UserBike).filter(
            UserBike.user_id == current_user.id,
            RideLog.ride_date >= start_date
        ).all()
        
        if not rides:
            return jsonify({
                'success': True,
                'message': 'No rides found in specified period',
                'data': {}
            }), 200
        
        # Calculate statistics
        total_distance = sum(ride.distance for ride in rides if ride.distance)
        total_duration = sum(ride.duration for ride in rides if ride.duration)
        avg_speed = sum(ride.avg_speed for ride in rides if ride.avg_speed) / len(rides)
        
        # Road type distribution
        road_types = {}
        for ride in rides:
            road_types[ride.road_type] = road_types.get(ride.road_type, 0) + 1
        
        # Riding style distribution
        riding_styles = {}
        for ride in rides:
            riding_styles[ride.riding_style] = riding_styles.get(ride.riding_style, 0) + 1
        
        patterns = {
            'period_days': days,
            'total_rides': len(rides),
            'total_distance_km': round(total_distance, 2),
            'total_duration_minutes': total_duration,
            'average_speed_kmh': round(avg_speed, 2),
            'road_type_distribution': road_types,
            'riding_style_distribution': riding_styles
        }
        
        return jsonify({
            'success': True,
            'data': patterns
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/brand-comparison', methods=['GET'])
def get_brand_comparison():
    """Compare statistics across brands"""
    try:
        brands = db.session.query(
            Bike.brand,
            func.count(Bike.id).label('model_count'),
            func.avg(Bike.price).label('avg_price'),
            func.avg(Review.rating).label('avg_rating')
        ).outerjoin(Review).filter(
            Bike.is_active == True
        ).group_by(Bike.brand).all()
        
        brand_data = []
        for brand, model_count, avg_price, avg_rating in brands:
            brand_data.append({
                'brand': brand,
                'model_count': model_count,
                'average_price': round(avg_price, 2) if avg_price else 0,
                'average_rating': round(avg_rating, 2) if avg_rating else 0
            })
        
        # Sort by model count
        brand_data.sort(key=lambda x: x['model_count'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': brand_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/monthly-trends', methods=['GET'])
def get_monthly_trends():
    """Get monthly platform trends"""
    try:
        months = request.args.get('months', 6, type=int)
        
        # Get new users per month
        user_trends = db.session.query(
            extract('year', User.created_at).label('year'),
            extract('month', User.created_at).label('month'),
            func.count(User.id).label('count')
        ).group_by('year', 'month').order_by('year', 'month').limit(months).all()
        
        # Get new reviews per month
        review_trends = db.session.query(
            extract('year', Review.created_at).label('year'),
            extract('month', Review.created_at).label('month'),
            func.count(Review.id).label('count')
        ).group_by('year', 'month').order_by('year', 'month').limit(months).all()
        
        trends = {
            'new_users': [
                {
                    'year': int(year),
                    'month': int(month),
                    'count': count
                }
                for year, month, count in user_trends
            ],
            'new_reviews': [
                {
                    'year': int(year),
                    'month': int(month),
                    'count': count
                }
                for year, month, count in review_trends
            ]
        }
        
        return jsonify({
            'success': True,
            'data': trends
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
