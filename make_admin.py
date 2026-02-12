"""
Quick script to make a user admin
"""
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    print("\n=== Make User Admin ===\n")
    
    # Show all users
    users = User.query.all()
    if not users:
        print("No users found. Please register first at http://127.0.0.1:5000/auth/register")
    else:
        print("Available users:")
        for i, user in enumerate(users, 1):
            role_badge = "👑 ADMIN" if user.role == 'admin' else "👤 USER"
            print(f"{i}. {user.username} ({user.email}) - {role_badge}")
        
        print("\n")
        choice = input("Enter user number to make admin (or 'q' to quit): ").strip()
        
        if choice.lower() != 'q' and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(users):
                user = users[idx]
                user.role = 'admin'
                db.session.commit()
                print(f"\n✅ {user.username} is now an ADMIN!")
                print(f"You can now access admin panel at: http://127.0.0.1:5000/admin")
            else:
                print("Invalid selection!")
        else:
            print("Cancelled.")
