from app.extensions import db
from app.models import CartItem, Product

class CartService:

    @staticmethod
    def get_cart_query(user_id=None, session_id=None):
        if user_id:
            return CartItem.query.filter_by(user_id=user_id)
        elif session_id:
            return CartItem.query.filter_by(session_id=session_id)
        return CartItem.query.filter(False)

    @classmethod
    def get_cart_summary(cls, user_id=None, session_id=None):
        raw_items = cls.get_cart_query(user_id, session_id).all()
        subtotal = round(sum(item.item_subtotal for item in raw_items), 2)
        shipping_fee = 0.0 if subtotal > 100.0 or subtotal == 0 else 15.0  # Free shipping over $100
        total = round(subtotal + shipping_fee, 2)
        total_count = sum(item.quantity for item in raw_items)

        return {
            'items': [item.to_dict() for item in raw_items],
            'subtotal': subtotal,
            'shipping_fee': shipping_fee,
            'total': total,
            'total_count': total_count
        }

    @classmethod
    def add_to_cart(cls, product_id, size, quantity=1, user_id=None, session_id=None):
        product = db.session.get(Product, product_id)
        if not product:
            return False, "Product not found."

        if product.stock_quantity <= 0:
            return False, f"Sorry, '{product.name}' is out of stock."

        # Validate requested size is available for product
        sizes = product.sizes_list
        target_size = str(size)
        if target_size not in [str(s) for s in sizes] and sizes:
            target_size = str(sizes[0])  # Fallback to first available size if size requested is generic

        # Find existing cart item for user/session with same product and size
        cart_query = cls.get_cart_query(user_id, session_id)
        existing_item = cart_query.filter_by(product_id=product_id, size=target_size).first()

        new_quantity = quantity
        if existing_item:
            new_quantity += existing_item.quantity

        if new_quantity > product.stock_quantity:
            return False, f"Only {product.stock_quantity} unit(s) available in stock."

        if existing_item:
            existing_item.quantity = new_quantity
        else:
            cart_item = CartItem(
                user_id=user_id,
                session_id=session_id if not user_id else None,
                product_id=product_id,
                size=target_size,
                quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()
        return True, "Product added to shopping bag successfully."

    @classmethod
    def update_cart_item(cls, item_id, quantity, user_id=None, session_id=None):
        if quantity <= 0:
            return cls.remove_from_cart(item_id, user_id, session_id)

        cart_query = cls.get_cart_query(user_id, session_id)
        item = cart_query.filter_by(id=item_id).first()

        if not item:
            return False, "Cart item not found."

        if quantity > item.product.stock_quantity:
            return False, f"Cannot update. Only {item.product.stock_quantity} available in stock."

        item.quantity = quantity
        db.session.commit()
        return True, "Cart updated successfully."

    @classmethod
    def remove_from_cart(cls, item_id, user_id=None, session_id=None):
        cart_query = cls.get_cart_query(user_id, session_id)
        item = cart_query.filter_by(id=item_id).first()

        if not item:
            return False, "Cart item not found."

        db.session.delete(item)
        db.session.commit()
        return True, "Item removed from cart."

    @classmethod
    def clear_cart(cls, user_id=None, session_id=None):
        items = cls.get_cart_query(user_id, session_id).all()
        for item in items:
            db.session.delete(item)
        db.session.commit()

    @classmethod
    def merge_guest_cart_to_user(cls, session_id, user_id):
        if not session_id or not user_id:
            return
        
        guest_items = CartItem.query.filter_by(session_id=session_id).all()
        for g_item in guest_items:
            cls.add_to_cart(
                product_id=g_item.product_id,
                size=g_item.size,
                quantity=g_item.quantity,
                user_id=user_id
            )
            db.session.delete(g_item)
        db.session.commit()
