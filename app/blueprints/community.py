from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.reviews import Review
from app.models.bike import Bike
from app.models.user_bikes import UserBike

community_bp = Blueprint('community', __name__)

@community_bp.route('/')
def index():
    reviews = Review.query.order_by(
        Review.created_at.desc()
    ).limit(20).all()
    return render_template('community/reviews.html', reviews=reviews)

@community_bp.route('/post-review', methods=['GET', 'POST'])
@login_required
def post_review():
    if request.method == 'POST':
        try:
            # Get form data
            bike_id = request.form.get('bike_id', type=int)
            rating = request.form.get('rating', type=int)
            title = request.form.get('title')
            content = request.form.get('content')
            
            # Validate required fields
            if not bike_id:
                flash('Please select a bike to review.', 'error')
                return redirect(url_for('community.post_review'))
            
            if not rating or rating < 1 or rating > 5:
                flash('Please provide a valid overall rating (1-5).', 'error')
                return redirect(url_for('community.post_review'))
            
            if not title or not title.strip():
                flash('Please provide a review title.', 'error')
                return redirect(url_for('community.post_review'))
            
            if not content or len(content.strip()) < 100:
                flash('Review content must be at least 100 characters long.', 'error')
                return redirect(url_for('community.post_review'))
            
            # Create review
            review = Review(
                user_id=current_user.id,
                bike_id=bike_id,
                rating=rating,
                title=title.strip(),
                content=content.strip(),
                performance_rating=request.form.get('performance_rating', type=int, default=3),
                comfort_rating=request.form.get('comfort_rating', type=int, default=3),
                mileage_rating=request.form.get('mileage_rating', type=int, default=3),
                looks_rating=request.form.get('looks_rating', type=int, default=3),
                ownership_duration=request.form.get('ownership_duration'),
                km_driven=request.form.get('km_driven', type=int),
                pros=request.form.get('pros'),
                cons=request.form.get('cons'),
                is_verified=True  # Auto-approve reviews for real-time display
            )
            
            db.session.add(review)
            db.session.commit()
            
            flash('Review posted successfully! 🎉', 'success')
            return redirect(url_for('community.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting review: {str(e)}', 'error')
            print(f"Error in post_review: {str(e)}")  # Debug print
            return redirect(url_for('community.post_review'))
    
    # GET request - show form
    user_bikes = UserBike.query.filter_by(user_id=current_user.id).all() if current_user.is_authenticated else []
    all_bikes = Bike.query.filter_by(is_active=True).order_by(Bike.brand, Bike.model).all()
    
    return render_template('community/post_review.html', user_bikes=user_bikes, all_bikes=all_bikes)

@community_bp.route('/review/<int:review_id>')
def single_review(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('community/single_review.html', review=review)
