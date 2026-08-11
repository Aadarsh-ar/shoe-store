def test_get_products_list(client):
    response = client.get('/api/products')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['products']) >= 1
    assert data['products'][0]['name'] == "Test Shoe Pro"

def test_get_product_detail(client):
    response = client.get('/api/products/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['product']['id'] == 1
    assert data['product']['brand'] == "TestBrand"

def test_product_search(client):
    response = client.get('/api/products?q=TestBrand')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['products']) == 1
