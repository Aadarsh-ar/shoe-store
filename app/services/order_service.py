from app.extensions import db
from app.models import Order, OrderItem, CartItem, Product
from app.services.cart_service import CartService
from app.services.inventory_service import InventoryService

class OrderService:

    @staticmethod
    def create_order(user_id, checkout_data):
        """
        Atomic transaction to create order from cart, update stock, and clear cart.
        """
        # Fetch cart items
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return False, "Your shopping cart is empty.", None

        # 1. Validate Stock
        valid, err_msg = InventoryService.check_and_reserve_stock(cart_items)
        if not valid:
            return False, err_msg, None

        # 2. Calculate Totals
        subtotal = round(sum(item.item_subtotal for item in cart_items), 2)
        shipping_fee = 0.0 if subtotal > 100.0 else 15.0
        total_amount = round(subtotal + shipping_fee, 2)

        try:
            # 3. Create Order Object
            order = Order(
                order_number=Order.generate_order_number(),
                user_id=user_id,
                status='Confirmed',
                subtotal=subtotal,
                shipping_fee=shipping_fee,
                total_amount=total_amount,
                full_name=checkout_data.get('full_name'),
                email=checkout_data.get('email'),
                phone=checkout_data.get('phone'),
                shipping_address=checkout_data.get('shipping_address'),
                city=checkout_data.get('city'),
                postal_code=checkout_data.get('postal_code'),
                country=checkout_data.get('country', 'United States'),
                payment_method=checkout_data.get('payment_method', 'Credit Card (Mock)'),
                payment_status='Paid'
            )
            db.session.add(order)
            db.session.flush()  # Generate order.id

            # 4. Create OrderItems & Deduct Stock
            for cart_item in cart_items:
                product = cart_item.product
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    product_image=product.image_url,
                    price=product.effective_price,
                    size=cart_item.size,
                    quantity=cart_item.quantity
                )
                db.session.add(order_item)

                # Stock deduction
                product.stock_quantity -= cart_item.quantity

                # Clear cart item
                db.session.delete(cart_item)

            # 5. Commit Transaction
            db.session.commit()
            return True, "Order placed successfully!", order

        except Exception as e:
            db.session.rollback()
            return False, f"Failed to place order: {str(e)}", None

    @staticmethod
    def get_user_orders(user_id):
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    @staticmethod
    def get_order_by_number(order_number, user_id=None):
        query = Order.query.filter_by(order_number=order_number)
        if user_id:
            query = query.filter_by(user_id=user_id)
        return query.first()

    @staticmethod
    def update_order_status(order_id, new_status):
        valid_statuses = ['Pending', 'Confirmed', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
        if new_status not in valid_statuses:
            return False, f"Invalid status. Must be one of {valid_statuses}"

        order = db.session.get(Order, order_id)
        if not order:
            return False, "Order not found."

        # If order cancelled, return inventory stock
        if new_status == 'Cancelled' and order.status != 'Cancelled':
            for item in order.items:
                if item.product_id:
                    product = db.session.get(Product, item.product_id)
                    if product:
                        product.stock_quantity += item.quantity

        order.status = new_status
        db.session.commit()
        return True, f"Order status updated to '{new_status}'."
