def test_admin_route_protection(client):
    # Log in as normal customer
    client.post('/api/auth/login', json={'email': 'customer@test.com', 'password': 'customer123'})

    # Try accessing admin product creation API
    response = client.post('/admin/api/products', json={
        'name': 'Unauthorized Shoe',
        'brand': 'FakeBrand',
        'price': 100,
        'category_id': 1
    })
    assert response.status_code == 403

def test_admin_product_crud(client):
    # Log in as Admin
    client.post('/api/auth/login', json={'email': 'admin@test.com', 'password': 'admin123'})

    # Create Product
    response = client.post('/admin/api/products', json={
        'name': 'Admin Exclusive Shoe',
        'brand': 'AdminBrand',
        'description': 'Super high end',
        'price': 250.00,
        'category_id': 1,
        'stock_quantity': 15,
        'available_sizes': '8,9,10,11'
    })
    assert response.status_code == 201
    prod_id = response.get_json()['product']['id']

    # Update Stock
    response = client.put(f'/admin/api/products/{prod_id}/stock', json={'stock_quantity': 50})
    assert response.status_code == 200

    # Delete Product
    response = client.delete(f'/admin/api/products/{prod_id}')
    assert response.status_code == 200
