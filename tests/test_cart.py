def test_cart_add_and_update(client):
    # Log in as customer
    client.post('/api/auth/login', json={'email': 'customer@test.com', 'password': 'customer123'})

    # Add product 1 size 9
    response = client.post('/api/cart', json={
        'product_id': 1,
        'size': '9',
        'quantity': 2
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['cart']['total_count'] == 2

    # Get cart
    response = client.get('/api/cart')
    assert response.status_code == 200
    cart_data = response.get_json()
    item_id = cart_data['items'][0]['id']

    # Update item quantity
    response = client.put(f'/api/cart/{item_id}', json={'quantity': 3})
    assert response.status_code == 200
    assert response.get_json()['cart']['total_count'] == 3

    # Delete item
    response = client.delete(f'/api/cart/{item_id}')
    assert response.status_code == 200
    assert response.get_json()['cart']['total_count'] == 0

def test_stock_limit_in_cart(client):
    client.post('/api/auth/login', json={'email': 'customer@test.com', 'password': 'customer123'})

    # Try adding more quantity than available stock (stock is 10)
    response = client.post('/api/cart', json={
        'product_id': 1,
        'size': '9',
        'quantity': 99
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "available in stock" in data['error']
