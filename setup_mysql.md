# MySQL Database Setup Guide

## Step 1: Install MySQL

### Option A: Download MySQL Installer
1. Visit: https://dev.mysql.com/downloads/installer/
2. Download MySQL Installer for Windows
3. Run the installer and choose "Developer Default" or "Server only"
4. Set a root password during installation (remember this!)

### Option B: Use XAMPP (Easier for beginners)
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP
3. Start MySQL from XAMPP Control Panel

## Step 2: Create the Database

### Using MySQL Command Line:
```bash
mysql -u root -p
```

Then run:
```sql
CREATE DATABASE sport_bike_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sportbike_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON sport_bike_db.* TO 'sportbike_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### OR use the provided Python script:
```bash
python create_mysql_db.py
```

## Step 3: Update .env File

Edit your `.env` file with your MySQL credentials:

```env
# For root user (not recommended for production)
DATABASE_URL=mysql+pymysql://root:your_root_password@localhost/sport_bike_db

# OR for dedicated user (recommended)
DATABASE_URL=mysql+pymysql://sportbike_user:your_password@localhost/sport_bike_db
```

## Step 4: Initialize Database Tables

Run the initialization script:
```bash
python init_db.py
```

## Step 5: Restart Your Flask Application

Stop the current server (Ctrl+C) and restart:
```bash
python run.py
```

## Troubleshooting

### Error: "Can't connect to MySQL server"
- Make sure MySQL service is running
- Check if you're using the correct port (default: 3306)
- Verify username and password

### Error: "Access denied for user"
- Double-check your username and password in .env
- Make sure the user has proper permissions

### Error: "Unknown database"
- Make sure you created the database (Step 2)
- Check database name in .env matches what you created

## Current Configuration

Your project is currently configured to use:
- Database: `sport_bike_db`
- Default connection: `mysql+pymysql://root:@localhost/sport_bike_db`

Update the password in `.env` file after installing MySQL.
