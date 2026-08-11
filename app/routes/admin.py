from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from sqlalchemy import func
from app.extensions import db
from app.models import User, Product, Category, Order, OrderItem
from app.routes.auth import admin_required
from app.services.inventory_service import InventoryService
from app.services.order_service import OrderService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    
    # Calculate Total Revenue from Confirmed/Shipped/Delivered orders
    revenue = db.session.query(func.sum(Order.total_amount))\
        .filter(Order.status != 'Cancelled')\
        .scalar() or 0.0

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    low_stock_products = Product.query.filter(Product.stock_quantity <= 10).order_by(Product.stock_quantity.asc()).all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_products=total_products,
        total_orders=total_orders,
        revenue=round(revenue, 2),
        recent_orders=recent_orders,
        low_stock_products=low_stock_products
    )

@admin_bp.route('/products')
@admin_required
def products_list():
    products = Product.query.order_by(Product.id.desc()).all()
    categories = Category.query.all()
    return render_template('admin/products.html', products=products, categories=categories)

@admin_bp.route('/orders')
@admin_required
def orders_list():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/users')
@admin_required
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/inventory')
@admin_required
def inventory_list():
    products = Product.query.order_by(Product.stock_quantity.asc()).all()
    return render_template('admin/inventory.html', products=products)


# --- REST API ADMIN ENDPOINTS ---

@admin_bp.route('/api/products', methods=['POST'])
@admin_required
def api_create_product():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    brand = data.get('brand', '').strip()
    description = data.get('description', '').strip()
    price = data.get('price')
    discount_price = data.get('discount_price')
    category_id = data.get('category_id')
    available_sizes = data.get('available_sizes', '7,8,9,10,11')
    color = data.get('color', 'Black')
    image_url = data.get('image_url', '/static/images/placeholder_shoe.svg')
    stock_quantity = data.get('stock_quantity', 0)

    if not name or not brand or price is None or not category_id:
        return jsonify({'error': 'Name, brand, price, and category_id are required'}), 400

    try:
        product = Product(
            name=name,
            brand=brand,
            description=description,
            price=float(price),
            discount_price=float(discount_price) if discount_price else None,
            category_id=int(category_id),
            color=color,
            image_url=image_url,
            stock_quantity=int(stock_quantity),
            is_featured=data.get('is_featured', False)
        )
        product.sizes_list = available_sizes if isinstance(available_sizes, list) else [s.strip() for s in available_sizes.split(',')]
        
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully', 'product': product.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/api/products/<int:product_id>', methods=['PUT'])
@admin_required
def api_update_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}
    if 'name' in data: product.name = data['name'].strip()
    if 'brand' in data: product.brand = data['brand'].strip()
    if 'description' in data: product.description = data['description'].strip()
    if 'price' in data: product.price = float(data['price'])
    if 'discount_price' in data: product.discount_price = float(data['discount_price']) if data['discount_price'] else None
    if 'category_id' in data: product.category_id = int(data['category_id'])
    if 'available_sizes' in data:
        product.sizes_list = data['available_sizes'] if isinstance(data['available_sizes'], list) else [s.strip() for s in data['available_sizes'].split(',')]
    if 'color' in data: product.color = data['color']
    if 'image_url' in data: product.image_url = data['image_url']
    if 'stock_quantity' in data: product.stock_quantity = int(data['stock_quantity'])
    if 'is_featured' in data: product.is_featured = bool(data['is_featured'])

    db.session.commit()
    return jsonify({'message': 'Product updated successfully', 'product': product.to_dict()}), 200

@admin_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@admin_required
def api_delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

@admin_bp.route('/api/products/<int:product_id>/stock', methods=['PUT'])
@admin_required
def api_update_stock(product_id):
    data = request.get_json() or {}
    stock_quantity = data.get('stock_quantity')
    if stock_quantity is None:
        return jsonify({'error': 'stock_quantity is required'}), 400

    success, message = InventoryService.update_product_stock(product_id, int(stock_quantity))
    if not success:
        return jsonify({'error': message}), 400

    return jsonify({'message': message}), 200

@admin_bp.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@admin_required
def api_update_order_status(order_id):
    data = request.get_json() or {}
    status = data.get('status')
    if not status:
        return jsonify({'error': 'status parameter is required'}), 400

    success, message = OrderService.update_order_status(order_id, status)
    if not success:
        return jsonify({'error': message}), 400

    return jsonify({'message': message}), 200
