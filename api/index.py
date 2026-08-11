import os
import sys

# Ensure root project directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

app = create_app('production')

# Seed database on cold start if database is empty
with app.app_context():
    try:
        db.create_all()
        from app.models import User
        if not User.query.filter_by(email="theaaadarsh15@gmail.com").first():
            from seed import seed_database
            seed_database()
    except Exception as e:
        print("Vercel DB initialization warning:", e)
