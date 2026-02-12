"""
Add seller details columns to users table
Run this script to add new seller detail fields to the database
"""
from app import create_app, db
from sqlalchemy import text

app = create_app()

def add_seller_details_columns():
    with app.app_context():
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('users')]
            
            columns_to_add = {
                'rc_full_name': 'VARCHAR(100)',
                'address': 'TEXT',
                'id_proof_type': 'VARCHAR(50)',
                'id_proof_number': 'VARCHAR(50)'
            }
            
            for column_name, column_type in columns_to_add.items():
                if column_name not in existing_columns:
                    sql = f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
                    db.session.execute(text(sql))
                    print(f"✓ Added column: {column_name}")
                else:
                    print(f"⊘ Column already exists: {column_name}")
            
            db.session.commit()
            print("\n✓ Seller details columns added successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error: {str(e)}")

if __name__ == '__main__':
    print("Adding seller details columns to users table...\n")
    add_seller_details_columns()
