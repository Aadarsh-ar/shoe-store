import os
import sys
import tempfile

# Ensure root project directory is in python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

# Force VERCEL env flag so config.py writes DB to /tmp
os.environ.setdefault('VERCEL', '1')

# Explicitly set DATABASE_URL to a writable /tmp path if not already set
if not os.environ.get('DATABASE_URL'):
    db_path = os.path.join(tempfile.gettempdir(), 'shoestore.db')
    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'

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
