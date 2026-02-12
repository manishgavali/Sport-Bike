"""
Reset user password
"""
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    print("\n=== Reset User Password ===\n")
    
    username = input("Enter username (default: manish): ").strip() or 'manish'
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        print(f"❌ User '{username}' not found!")
        print("\nAvailable users:")
        users = User.query.all()
        for u in users:
            print(f"  - {u.username} ({u.email})")
    else:
        print(f"Found user: {user.username} ({user.email})")
        print(f"Role: {user.role}")
        
        new_password = input("\nEnter new password (default: manish123): ").strip() or 'manish123'
        
        user.set_password(new_password)
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ Password reset successfully!")
        print("="*50)
        print(f"USERNAME: {user.username}")
        print(f"PASSWORD: {new_password}")
        print("="*50)
        print("\nLogin at: http://127.0.0.1:5000/auth/login")
