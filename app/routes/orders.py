from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.services.cart_service import CartService
from app.services.order_service import OrderService

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_summary = CartService.get_cart_summary(user_id=current_user.id)
    if not cart_summary['items']:
        flash('Your cart is empty. Add shoes to cart before checkout.', 'warning')
        return redirect(url_for('products.catalogue'))

    if request.method == 'POST':
        checkout_data = {
            'full_name': request.form.get('full_name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'shipping_address': request.form.get('shipping_address', '').strip(),
            'city': request.form.get('city', '').strip(),
            'postal_code': request.form.get('postal_code', '').strip(),
            'country': request.form.get('country', 'United States'),
            'payment_method': request.form.get('payment_method', 'Credit Card (Mock)')
        }

        # Validation
        for field in ['full_name', 'email', 'phone', 'shipping_address', 'city', 'postal_code']:
            if not checkout_data[field]:
                flash(f"Please fill in all shipping details ({field.replace('_', ' ')} is required).", 'danger')
                return render_template('checkout.html', cart=cart_summary)

        success, message, order = OrderService.create_order(current_user.id, checkout_data)
        if success:
            flash(f"Order #{order.order_number} placed successfully!", 'success')
            return redirect(url_for('orders.order_detail', order_number=order.order_number))
        else:
            flash(message, 'danger')

    return render_template('checkout.html', cart=cart_summary)

@orders_bp.route('/orders')
@login_required
def order_history():
    user_orders = OrderService.get_user_orders(current_user.id)
    return render_template('orders.html', orders=user_orders)

@orders_bp.route('/orders/<string:order_number>')
@login_required
def order_detail(order_number):
    order = OrderService.get_order_by_number(order_number, user_id=current_user.id if not current_user.is_admin() else None)
    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('orders.order_history'))

    return render_template('orders.html', single_order=order, orders=OrderService.get_user_orders(current_user.id))

# --- REST API ENDPOINTS ---

@orders_bp.route('/api/orders', methods=['GET'])
@login_required
def api_get_orders():
    orders = OrderService.get_user_orders(current_user.id)
    return jsonify({
        'orders': [o.to_dict() for o in orders]
    }), 200

@orders_bp.route('/api/orders', methods=['POST'])
@login_required
def api_create_order():
    data = request.get_json() or {}
    success, message, order = OrderService.create_order(current_user.id, data)

    if not success:
        return jsonify({'error': message}), 400

    return jsonify({
        'message': message,
        'order': order.to_dict()
    }), 201

@orders_bp.route('/api/orders/<string:order_identifier>', methods=['GET'])
@login_required
def api_get_order(order_identifier):
    order = None
    if order_identifier.isdigit():
        order = OrderService.get_order_by_number(order_identifier, user_id=current_user.id if not current_user.is_admin() else None)
    
    if not order:
        order = OrderService.get_order_by_number(order_identifier, user_id=current_user.id if not current_user.is_admin() else None)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({'order': order.to_dict()}), 200
