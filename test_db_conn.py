from dotenv import load_dotenv
load_dotenv()

import os
print("DATABASE_URL from .env:", os.getenv('DATABASE_URL'))

from config import config
print("Config URI:", config['development'].SQLALCHEMY_DATABASE_URI)

from app import create_app, db

app = create_app('development')

with app.app_context():
    print("App DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("\nCreating all tables...")
    db.create_all()
    print("✅ Done!")
