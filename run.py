import os
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    print(f"ShoeStore Flask Server starting on http://0.0.0.0:{port} ...")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
