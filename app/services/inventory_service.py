from app.extensions import db
from app.models import Product

class InventoryService:

    @staticmethod
    def check_and_reserve_stock(items):
        """
        Validate that every product has enough stock.
        items: list of objects with product_id and quantity properties
        Returns: (success: bool, error_message: str or None)
        """
        for item in items:
            product = db.session.get(Product, item.product_id)
            if not product:
                return False, f"Product ID {item.product_id} no longer exists."
            if product.stock_quantity < item.quantity:
                return False, f"Insufficient stock for '{product.name}'. Available: {product.stock_quantity}, Requested: {item.quantity}."
        return True, None

    @staticmethod
    def reduce_stock(order_items):
        """
        Deduct product stock quantities according to order items.
        Must be called within an active DB transaction block.
        """
        for item in order_items:
            product = db.session.get(Product, item.product_id)
            if product:
                if product.stock_quantity < item.quantity:
                    raise ValueError(f"Cannot fulfill order: insufficient stock for '{product.name}'.")
                product.stock_quantity -= item.quantity

    @staticmethod
    def update_product_stock(product_id, new_quantity):
        if new_quantity < 0:
            return False, "Stock quantity cannot be negative."
        
        product = db.session.get(Product, product_id)
        if not product:
            return False, "Product not found."
            
        product.stock_quantity = new_quantity
        db.session.commit()
        return True, "Stock updated successfully."
