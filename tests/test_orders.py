from app.extensions import db
from app.models import Product

def test_order_creation_and_inventory_reduction(client, app):
    client.post('/api/auth/login', json={'email': 'customer@test.com', 'password': 'customer123'})

    # Add 2 pairs to cart
    client.post('/api/cart', json={'product_id': 1, 'size': '9', 'quantity': 2})

    # Place order
    response = client.post('/api/orders', json={
        'full_name': 'Customer User',
        'email': 'customer@test.com',
        'phone': '555-0199',
        'shipping_address': '456 Test Street',
        'city': 'TestCity',
        'postal_code': '90210',
        'country': 'United States',
        'payment_method': 'Credit Card (Mock)'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['order']['order_number'].startswith("ORD-")
    assert data['order']['total_amount'] > 0

    # Verify inventory was reduced from 10 to 8
    with app.app_context():
        p = db.session.get(Product, 1)
        assert p.stock_quantity == 8
