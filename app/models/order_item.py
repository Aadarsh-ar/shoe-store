from app.extensions import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product_name = db.Column(db.String(120), nullable=False)
    product_image = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    @property
    def item_total(self):
        return round(self.price * self.quantity, 2)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_image': self.product_image,
            'price': self.price,
            'size': self.size,
            'quantity': self.quantity,
            'total': self.item_total
        }

    def __repr__(self):
        return f'<OrderItem {self.product_name} x {self.quantity}>'
