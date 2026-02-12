"""
MySQL Database Creator
This script helps you create the MySQL database for the project.
Run this AFTER installing MySQL.
"""

import pymysql
import sys
from getpass import getpass

def create_database():
    """Create the MySQL database"""
    print("=" * 60)
    print("MySQL Database Setup for Smart Sport Bike Ecosystem")
    print("=" * 60)
    print()
    
    # Get MySQL credentials
    print("Enter your MySQL root credentials:")
    host = input("MySQL Host [localhost]: ").strip() or "localhost"
    port = input("MySQL Port [3306]: ").strip() or "3306"
    user = input("MySQL Root Username [root]: ").strip() or "root"
    password = getpass("MySQL Root Password: ")
    
    database_name = "sport_bike_db"
    
    try:
        # Connect to MySQL
        print(f"\nConnecting to MySQL at {host}:{port}...")
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password
        )
        
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
        result = cursor.fetchone()
        
        if result:
            print(f"\n⚠️  Database '{database_name}' already exists!")
            choice = input("Do you want to drop and recreate it? (yes/no): ").strip().lower()
            if choice == 'yes':
                cursor.execute(f"DROP DATABASE {database_name}")
                print(f"✅ Dropped existing database '{database_name}'")
            else:
                print("Keeping existing database.")
                connection.close()
                return
        
        # Create database
        print(f"\nCreating database '{database_name}'...")
        cursor.execute(
            f"CREATE DATABASE {database_name} "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print(f"✅ Database '{database_name}' created successfully!")
        
        # Ask if user wants to create a dedicated database user
        create_user = input("\nDo you want to create a dedicated database user? (yes/no): ").strip().lower()
        
        if create_user == 'yes':
            db_user = input("Enter username [sportbike_user]: ").strip() or "sportbike_user"
            db_pass = getpass("Enter password for this user: ")
            
            # Create user
            try:
                cursor.execute(f"DROP USER IF EXISTS '{db_user}'@'localhost'")
            except:
                pass
                
            cursor.execute(
                f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}'"
            )
            cursor.execute(
                f"GRANT ALL PRIVILEGES ON {database_name}.* TO '{db_user}'@'localhost'"
            )
            cursor.execute("FLUSH PRIVILEGES")
            
            print(f"\n✅ User '{db_user}' created successfully!")
            print("\n" + "=" * 60)
            print("Update your .env file with this connection string:")
            print("=" * 60)
            print(f"DATABASE_URL=mysql+pymysql://{db_user}:{db_pass}@{host}/{database_name}")
        else:
            print("\n" + "=" * 60)
            print("Update your .env file with this connection string:")
            print("=" * 60)
            print(f"DATABASE_URL=mysql+pymysql://{user}:{password}@{host}/{database_name}")
        
        print("=" * 60)
        print("\nNext steps:")
        print("1. Update your .env file with the DATABASE_URL above")
        print("2. Run: python init_db.py")
        print("3. Run: python run.py")
        print("=" * 60)
        
        cursor.close()
        connection.close()
        
    except pymysql.Error as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        create_database()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
