from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User

app = create_app('development')

with app.app_context():
    users = User.query.all()
    print(f"\n=== Total users in database: {len(users)} ===\n")
    
    for user in users:
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Active: {user.is_active}")
        print(f"Role: {user.role}")
        print("-" * 40)
    
    if len(users) == 0:
        print("No users found! You need to register first.")
