from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.products import products_bp
from app.routes.cart import cart_bp
from app.routes.wishlist import wishlist_bp
from app.routes.orders import orders_bp
from app.routes.admin import admin_bp

__all__ = [
    'main_bp',
    'auth_bp',
    'products_bp',
    'cart_bp',
    'wishlist_bp',
    'orders_bp',
    'admin_bp'
]
