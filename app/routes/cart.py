from flask import Blueprint, render_template, request, jsonify, session
from flask_login import current_user
from app.services.cart_service import CartService

cart_bp = Blueprint('cart', __name__)

def _get_cart_identifiers():
    user_id = current_user.id if current_user.is_authenticated else None
    session_id = session.get('session_id') if not user_id else None
    if not user_id and not session_id:
        import uuid
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    return user_id, session_id

@cart_bp.route('/cart')
def view_cart():
    user_id, session_id = _get_cart_identifiers()
    summary = CartService.get_cart_summary(user_id=user_id, session_id=session_id)
    return render_template('cart.html', cart=summary)

# --- REST API ENDPOINTS ---

@cart_bp.route('/api/cart', methods=['GET'])
def api_get_cart():
    user_id, session_id = _get_cart_identifiers()
    summary = CartService.get_cart_summary(user_id=user_id, session_id=session_id)
    return jsonify(summary), 200

@cart_bp.route('/api/cart', methods=['POST'])
def api_add_to_cart():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    size = data.get('size')
    quantity = data.get('quantity', 1)

    if not product_id or not size:
        return jsonify({'error': 'product_id and size are required'}), 400

    user_id, session_id = _get_cart_identifiers()
    success, message = CartService.add_to_cart(
        product_id=product_id,
        size=size,
        quantity=quantity,
        user_id=user_id,
        session_id=session_id
    )

    if not success:
        return jsonify({'error': message}), 400

    summary = CartService.get_cart_summary(user_id=user_id, session_id=session_id)
    return jsonify({
        'message': message,
        'cart': summary
    }), 200

@cart_bp.route('/api/cart/<int:item_id>', methods=['PUT'])
def api_update_cart(item_id):
    data = request.get_json() or {}
    quantity = data.get('quantity')

    if quantity is None:
        return jsonify({'error': 'quantity parameter required'}), 400

    user_id, session_id = _get_cart_identifiers()
    success, message = CartService.update_cart_item(
        item_id=item_id,
        quantity=quantity,
        user_id=user_id,
        session_id=session_id
    )

    if not success:
        return jsonify({'error': message}), 400

    summary = CartService.get_cart_summary(user_id=user_id, session_id=session_id)
    return jsonify({
        'message': message,
        'cart': summary
    }), 200

@cart_bp.route('/api/cart/<int:item_id>', methods=['DELETE'])
def api_delete_cart(item_id):
    user_id, session_id = _get_cart_identifiers()
    success, message = CartService.remove_from_cart(
        item_id=item_id,
        user_id=user_id,
        session_id=session_id
    )

    if not success:
        return jsonify({'error': message}), 404

    summary = CartService.get_cart_summary(user_id=user_id, session_id=session_id)
    return jsonify({
        'message': message,
        'cart': summary
    }), 200
