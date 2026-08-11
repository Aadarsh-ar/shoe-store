from datetime import datetime
from app.extensions import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=True, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def item_subtotal(self):
        if self.product:
            return round(self.product.effective_price * self.quantity, 2)
        return 0.0

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'size': self.size,
            'quantity': self.quantity,
            'subtotal': self.item_subtotal,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<CartItem user={self.user_id} product={self.product_id} size={self.size} qty={self.quantity}>'
