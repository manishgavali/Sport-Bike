from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        riding_experience = request.form.get('riding_experience', 'beginner')
        
        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            riding_experience=riding_experience
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        print("=== LOGIN ATTEMPT ===")
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        print(f"Username: {username}, Password length: {len(password) if password else 0}")
        
        # Optimized query - only load necessary columns for authentication
        user = User.query.filter_by(username=username).first()
        print(f"User found: {user is not None}")
        if user:
            print(f"User active: {user.is_active}")
            print(f"Password check: {user.check_password(password)}")
        
        if user and user.is_active and user.check_password(password):
            print("Login successful, calling login_user()")
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name or user.username}!', 'success')
            print(f"Redirecting to: {next_page or url_for('dashboard.index')}")
            return redirect(next_page or url_for('dashboard.index'))
        else:
            print("Login failed - invalid credentials or inactive user")
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    try:
        # Update basic details
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        current_user.riding_experience = request.form.get('riding_experience')
        
        # Update seller details
        current_user.rc_full_name = request.form.get('rc_full_name')
        current_user.address = request.form.get('address')
        current_user.id_proof_type = request.form.get('id_proof_type')
        current_user.id_proof_number = request.form.get('id_proof_number')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating profile: {str(e)}', 'error')
    
    return redirect(url_for('auth.profile'))
