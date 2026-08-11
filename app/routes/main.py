import uuid
from flask import Blueprint, render_template, session
from app.models import Category, Product
from app.services.product_service import ProductService

main_bp = Blueprint('main', __name__)

@main_bp.before_app_request
def ensure_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

@main_bp.route('/')
def index():
    categories = Category.query.all()
    featured_products = ProductService.get_featured_products(limit=8)
    new_arrivals = ProductService.get_new_arrivals(limit=8)
    
    return render_template(
        'index.html',
        categories=categories,
        featured_products=featured_products,
        new_arrivals=new_arrivals
    )
