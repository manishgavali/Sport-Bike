import re
from flask import flash

class Validator:
    """Validation utilities"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_username(username):
        """Validate username"""
        if len(username) < 3 or len(username) > 20:
            return False, "Username must be 3-20 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, "Valid"
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain a number"
        return True, "Valid"
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        pattern = r'^[6-9]\d{9}$'  # Indian phone number
        return re.match(pattern, phone) is not None
