from flask import jsonify, request
from app.api import api_bp
from app.models.bike import Bike
from app.models.bike_specs import BikeSpec
from app.models.reviews import Review
from app import db
from sqlalchemy import func

@api_bp.route('/bikes', methods=['GET'])
def get_bikes():
    """Get all bikes with optional filters"""
    try:
        # Query parameters for filtering
        brand = request.args.get('brand')
        category = request.args.get('category')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        min_cc = request.args.get('min_cc', type=int)
        max_cc = request.args.get('max_cc', type=int)
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Build query
        query = Bike.query.filter_by(is_active=True)
        
        if brand:
            query = query.filter(Bike.brand.ilike(f'%{brand}%'))
        
        if category:
            query = query.filter(Bike.category.ilike(f'%{category}%'))
        
        if min_price:
            query = query.filter(Bike.price >= min_price)
        
        if max_price:
            query = query.filter(Bike.price <= max_price)
        
        # Join with specs for CC filtering
        if min_cc or max_cc:
            query = query.join(BikeSpec)
            if min_cc:
                query = query.filter(BikeSpec.engine_cc >= min_cc)
            if max_cc:
                query = query.filter(BikeSpec.engine_cc <= max_cc)
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        bikes = query.limit(limit).offset(offset).all()
        
        # Serialize bikes
        bikes_data = []
        for bike in bikes:
            bike_dict = {
                'id': bike.id,
                'brand': bike.brand,
                'model': bike.model,
                'year': bike.year,
                'category': bike.category,
                'price': bike.price,
                'image_url': bike.image_url,
                'specs': None
            }
            
            if bike.specs:
                bike_dict['specs'] = {
                    'engine_cc': bike.specs.engine_cc,
                    'max_power': bike.specs.max_power,
                    'max_torque': bike.specs.max_torque,
                    'top_speed': bike.specs.top_speed,
                    'acceleration_0_100': bike.specs.acceleration_0_100,
                    'mileage_city': bike.specs.mileage_city,
                    'mileage_highway': bike.specs.mileage_highway,
                    'kerb_weight': bike.specs.kerb_weight,
                    'fuel_capacity': bike.specs.fuel_capacity,
                    'seat_height': bike.specs.seat_height
                }
            
            bikes_data.append(bike_dict)
        
        return jsonify({
            'success': True,
            'total_count': total_count,
            'returned_count': len(bikes_data),
            'limit': limit,
            'offset': offset,
            'data': bikes_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/bikes/<int:bike_id>', methods=['GET'])
def get_bike_details(bike_id):
    """Get detailed information about a specific bike"""
    try:
        bike = Bike.query.get_or_404(bike_id)
        
        # Calculate average rating
        avg_rating = db.session.query(func.avg(Review.rating)).filter_by(
            bike_id=bike_id, 
            is_verified=True
        ).scalar() or 0
        
        # Get review count
        review_count = Review.query.filter_by(
            bike_id=bike_id, 
            is_verified=True
        ).count()
        
        # Get recent reviews
        recent_reviews = Review.query.filter_by(
            bike_id=bike_id, 
            is_verified=True
        ).order_by(Review.created_at.desc()).limit(5).all()
        
        reviews_data = []
        for review in recent_reviews:
            reviews_data.append({
                'id': review.id,
                'rating': review.rating,
                'title': review.title,
                'content': review.content[:200],
                'author': review.author.username,
                'created_at': review.created_at.strftime('%Y-%m-%d')
            })
        
        bike_data = {
            'id': bike.id,
            'brand': bike.brand,
            'model': bike.model,
            'year': bike.year,
            'category': bike.category,
            'price': bike.price,
            'image_url': bike.image_url,
            'ratings': {
                'average': round(avg_rating, 2),
                'count': review_count
            },
            'recent_reviews': reviews_data
        }
        
        if bike.specs:
            bike_data['specifications'] = {
                'engine': {
                    'cc': bike.specs.engine_cc,
                    'type': bike.specs.engine_type,
                    'max_power': bike.specs.max_power,
                    'max_power_rpm': bike.specs.max_power_rpm,
                    'max_torque': bike.specs.max_torque,
                    'max_torque_rpm': bike.specs.max_torque_rpm,
                    'fuel_system': bike.specs.fuel_system
                },
                'performance': {
                    'top_speed': bike.specs.top_speed,
                    'acceleration_0_100': bike.specs.acceleration_0_100,
                    'mileage_city': bike.specs.mileage_city,
                    'mileage_highway': bike.specs.mileage_highway
                },
                'dimensions': {
                    'length': bike.specs.length,
                    'width': bike.specs.width,
                    'height': bike.specs.height,
                    'wheelbase': bike.specs.wheelbase,
                    'ground_clearance': bike.specs.ground_clearance,
                    'seat_height': bike.specs.seat_height,
                    'kerb_weight': bike.specs.kerb_weight,
                    'fuel_capacity': bike.specs.fuel_capacity
                },
                'brakes_suspension': {
                    'front_brake': bike.specs.front_brake,
                    'rear_brake': bike.specs.rear_brake,
                    'front_suspension': bike.specs.front_suspension,
                    'rear_suspension': bike.specs.rear_suspension
                },
                'tyres': {
                    'front': bike.specs.front_tyre,
                    'rear': bike.specs.rear_tyre
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


@api_bp.route('/bikes/compare', methods=['POST'])
def compare_bikes():
    """Compare multiple bikes"""
    try:
        data = request.get_json()
        bike_ids = data.get('bike_ids', [])
        
        if len(bike_ids) < 2:
            return jsonify({
                'success': False,
                'error': 'At least 2 bike IDs required for comparison'
            }), 400
        
        bikes = Bike.query.filter(Bike.id.in_(bike_ids)).all()
        
        if len(bikes) < 2:
            return jsonify({
                'success': False,
                'error': 'Invalid bike IDs provided'
            }), 400
        
        comparison_data = []
        
        for bike in bikes:
            bike_comparison = {
                'id': bike.id,
                'name': f"{bike.brand} {bike.model}",
                'price': bike.price,
                'specifications': {}
            }
            
            if bike.specs:
                bike_comparison['specifications'] = {
                    'engine_cc': bike.specs.engine_cc,
                    'max_power': bike.specs.max_power,
                    'max_torque': bike.specs.max_torque,
                    'top_speed': bike.specs.top_speed,
                    'acceleration_0_100': bike.specs.acceleration_0_100,
                    'mileage_avg': (bike.specs.mileage_city + bike.specs.mileage_highway) / 2,
                    'kerb_weight': bike.specs.kerb_weight,
                    'fuel_capacity': bike.specs.fuel_capacity
                }
            
            comparison_data.append(bike_comparison)
        
        return jsonify({
            'success': True,
            'data': comparison_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/bikes/search', methods=['GET'])
def search_bikes():
    """Search bikes by keyword"""
    try:
        query = request.args.get('q', '')
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query required'
            }), 400
        
        bikes = Bike.query.filter(
            db.or_(
                Bike.brand.ilike(f'%{query}%'),
                Bike.model.ilike(f'%{query}%'),
                Bike.category.ilike(f'%{query}%')
            )
        ).filter_by(is_active=True).limit(limit).all()
        
        results = []
        for bike in bikes:
            results.append({
                'id': bike.id,
                'brand': bike.brand,
                'model': bike.model,
                'year': bike.year,
                'price': bike.price,
                'category': bike.category
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(results),
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/bikes/categories', methods=['GET'])
def get_categories():
    """Get all bike categories"""
    try:
        categories = db.session.query(
            Bike.category, 
            func.count(Bike.id).label('count')
        ).filter_by(is_active=True).group_by(Bike.category).all()
        
        categories_data = [
            {'category': cat, 'count': count} 
            for cat, count in categories if cat
        ]
        
        return jsonify({
            'success': True,
            'data': categories_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/bikes/brands', methods=['GET'])
def get_brands():
    """Get all bike brands"""
    try:
        brands = db.session.query(
            Bike.brand, 
            func.count(Bike.id).label('count')
        ).filter_by(is_active=True).group_by(Bike.brand).all()
        
        brands_data = [
            {'brand': brand, 'count': count} 
            for brand, count in brands
        ]
        
        return jsonify({
            'success': True,
            'data': brands_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
