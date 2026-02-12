from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    profile_image = db.Column(db.String(255), default='default.jpg')
    role = db.Column(db.String(20), default='user')  # user, admin
    riding_experience = db.Column(db.String(50))  # beginner, intermediate, expert
    
    # Seller Details (for resale marketplace)
    rc_full_name = db.Column(db.String(100))  # Full name as per RC
    address = db.Column(db.Text)  # Address as per RC or current address
    id_proof_type = db.Column(db.String(50))  # aadhaar, pan, voter_id, driving_license
    id_proof_number = db.Column(db.String(50))  # ID proof number
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    user_bikes = db.relationship('UserBike', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    accident_reports = db.relationship('AccidentReport', backref='reporter', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256:1000')
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'
