import os
from flask import Flask, render_template, request, jsonify
from app.config import config_by_name
from app.extensions import db, migrate, login_manager, csrf

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'app', 'templates')
    static_dir = os.path.join(base_dir, 'app', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize Flask Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Setup User Loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.wishlist import wishlist_bp
    from app.routes.orders import orders_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Disable CSRF on API blueprints so REST JSON calls execute seamlessly
    csrf.exempt(auth_bp)
    csrf.exempt(products_bp)
    csrf.exempt(cart_bp)
    csrf.exempt(wishlist_bp)
    csrf.exempt(orders_bp)
    csrf.exempt(admin_bp)

    # Global Context Processor
    @app.context_processor
    def inject_global_data():
        from flask_login import current_user
        from flask import session
        from app.services.cart_service import CartService
        from app.models import WishlistItem

        user_id = current_user.id if current_user.is_authenticated else None
        session_id = session.get('session_id')
        
        cart_summary = CartService.get_cart_summary(user_id=user_id, session_id=session_id)
        wishlist_count = WishlistItem.query.filter_by(user_id=user_id).count() if user_id else 0

        return {
            'cart_count': cart_summary['total_count'],
            'wishlist_count': wishlist_count
        }

    # Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Resource not found'}), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500

    return app
