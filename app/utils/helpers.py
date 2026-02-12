from datetime import datetime
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_currency(amount):
    """Format amount as INR currency"""
    return f"₹{amount:,.2f}"

def format_date(date):
    """Format date for display"""
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%d %B, %Y')

def calculate_percentage(part, whole):
    """Calculate percentage"""
    if whole == 0:
        return 0
    return (part / whole) * 100

def save_uploaded_file(file, upload_folder):
    """Save uploaded file securely"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filename
    return None
