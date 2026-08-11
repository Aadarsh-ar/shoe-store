from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models import WishlistItem, Product
from app.services.cart_service import CartService

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist')
@login_required
def view_wishlist():
    items = WishlistItem.query.filter_by(user_id=current_user.id).order_by(WishlistItem.created_at.desc()).all()
    return render_template('wishlist.html', wishlist_items=items)

# --- REST API ENDPOINTS ---

@wishlist_bp.route('/api/wishlist', methods=['GET'])
@login_required
def api_get_wishlist():
    items = WishlistItem.query.filter_by(user_id=current_user.id).order_by(WishlistItem.created_at.desc()).all()
    return jsonify({
        'wishlist': [item.to_dict() for item in items],
        'total_count': len(items)
    }), 200

@wishlist_bp.route('/api/wishlist', methods=['POST'])
@login_required
def api_add_to_wishlist():
    data = request.get_json() or {}
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'product_id is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    existing = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        return jsonify({'message': 'Product is already in your wishlist'}), 200

    wishlist_item = WishlistItem(user_id=current_user.id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()

    return jsonify({
        'message': 'Product added to wishlist',
        'wishlist_item': wishlist_item.to_dict()
    }), 201

@wishlist_bp.route('/api/wishlist/<int:item_id>', methods=['DELETE'])
@login_required
def api_remove_from_wishlist(item_id):
    item = WishlistItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Wishlist item not found'}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item removed from wishlist'}), 200

@wishlist_bp.route('/api/wishlist/<int:item_id>/move-to-cart', methods=['POST'])
@login_required
def api_move_to_cart(item_id):
    data = request.get_json() or {}
    size = data.get('size')

    item = WishlistItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Wishlist item not found'}), 404

    product = item.product
    if not size:
        # Default to first available size
        sizes = product.sizes_list
        size = sizes[0] if sizes else "9"

    success, message = CartService.add_to_cart(
        product_id=product.id,
        size=size,
        quantity=1,
        user_id=current_user.id
    )

    if not success:
        return jsonify({'error': message}), 400

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        'message': f"'{product.name}' moved to cart successfully!"
    }), 200
