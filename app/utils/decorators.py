from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin():
            flash('Admin access required', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def verified_user_required(f):
    """Decorator to require verified user"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_active:
            flash('Your account is not active', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
