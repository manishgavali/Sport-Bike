"""
Reset admin password
"""
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    print("\n=== Admin Account Info ===\n")
    
    # Find admin users
    admins = User.query.filter_by(role='admin').all()
    
    if not admins:
        print("No admin users found!")
        print("\nCreating default admin account...")
        admin = User(
            username='admin',
            email='admin@sportbike.com',
            full_name='System Admin',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin account created!")
        print("\n" + "="*50)
        print("USERNAME: admin")
        print("PASSWORD: admin123")
        print("="*50)
        print("\nLogin at: http://127.0.0.1:5000/auth/login")
    else:
        print("Found admin users:")
        for i, admin in enumerate(admins, 1):
            print(f"{i}. Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print()
        
        print("="*50)
        choice = input("Reset password for admin? (y/n): ").strip().lower()
        
        if choice == 'y':
            admin = admins[0]
            new_password = input("Enter new password (or press Enter for 'admin123'): ").strip()
            if not new_password:
                new_password = 'admin123'
            
            admin.set_password(new_password)
            db.session.commit()
            
            print("\n✅ Password reset successful!")
            print("\n" + "="*50)
            print(f"USERNAME: {admin.username}")
            print(f"PASSWORD: {new_password}")
            print("="*50)
            print("\nLogin at: http://127.0.0.1:5000/auth/login")
        else:
            print("\nNo changes made.")
            print("\nIf you forgot your password, run this script again.")
