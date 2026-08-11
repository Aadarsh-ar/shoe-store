import json
from datetime import datetime
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    brand = db.Column(db.String(60), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    available_sizes = db.Column(db.String(255), nullable=False, default="7,8,9,10,11") # Comma-separated sizes or JSON
    color = db.Column(db.String(50), nullable=False, default="Black")
    gender = db.Column(db.String(20), nullable=False, default="Unisex") # 'Men', 'Women', 'Kids', 'Unisex'
    image_url = db.Column(db.String(255), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Float, nullable=False, default=4.5)
    is_featured = db.Column(db.Boolean, default=False)
    is_new_release = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    wishlist_items = db.relationship('WishlistItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')

    @property
    def sizes_list(self):
        if not self.available_sizes:
            return []
        try:
            # Check if stored as JSON list
            return json.loads(self.available_sizes)
        except (json.JSONDecodeError, TypeError):
            # Fallback string splitting
            return [s.strip() for s in self.available_sizes.split(',') if s.strip()]

    @sizes_list.setter
    def sizes_list(self, sizes):
        if isinstance(sizes, list):
            self.available_sizes = json.dumps(sizes)
        else:
            self.available_sizes = str(sizes)

    @property
    def effective_price(self):
        if self.discount_price and self.discount_price > 0 and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'description': self.description,
            'price': self.price,
            'discount_price': self.discount_price,
            'effective_price': self.effective_price,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'sizes': self.sizes_list,
            'color': self.color,
            'gender': self.gender,
            'image_url': self.image_url,
            'stock_quantity': self.stock_quantity,
            'rating': self.rating,
            'is_featured': self.is_featured,
            'is_new_release': self.is_new_release,
            'is_in_stock': self.is_in_stock,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Product {self.name} (${self.price})>'
