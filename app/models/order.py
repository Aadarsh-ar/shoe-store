import uuid
from datetime import datetime
from app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Order Status: 'Pending', 'Confirmed', 'Processing', 'Shipped', 'Delivered', 'Cancelled'
    status = db.Column(db.String(30), nullable=False, default='Pending')
    
    subtotal = db.Column(db.Float, nullable=False, default=0.0)
    shipping_fee = db.Column(db.Float, nullable=False, default=0.0)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    
    # Shipping & Contact Details
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(60), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(60), nullable=False, default='United States')
    
    # Payment details
    payment_method = db.Column(db.String(50), nullable=False, default='Credit Card (Mock)')
    payment_status = db.Column(db.String(30), nullable=False, default='Paid')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def generate_order_number():
        date_str = datetime.utcnow().strftime('%Y%m%d')
        unique_suffix = uuid.uuid4().hex[:6].upper()
        return f"ORD-{date_str}-{unique_suffix}"

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'status': self.status,
            'subtotal': self.subtotal,
            'shipping_fee': self.shipping_fee,
            'total_amount': self.total_amount,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'shipping_address': self.shipping_address,
            'city': self.city,
            'postal_code': self.postal_code,
            'country': self.country,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Order {self.order_number} (${self.total_amount})>'
