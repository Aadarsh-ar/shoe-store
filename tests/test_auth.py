from app.models import User

def test_user_registration(client):
    response = client.post('/api/auth/register', json={
        'full_name': 'New User',
        'email': 'newuser@test.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['user']['email'] == 'newuser@test.com'
    assert data['user']['role'] == 'customer'

def test_user_login_success(client):
    response = client.post('/api/auth/login', json={
        'email': 'customer@test.com',
        'password': 'customer123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['email'] == 'customer@test.com'

def test_user_login_failure(client):
    response = client.post('/api/auth/login', json={
        'email': 'customer@test.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_user_logout(client):
    # Login first
    client.post('/api/auth/login', json={'email': 'customer@test.com', 'password': 'customer123'})
    response = client.post('/api/auth/logout')
    assert response.status_code == 200
