def test_register_user(client):
    response = client.post('/api/users/register', json={
        'full_name': 'Tester User',
        'email': 'tester@mail.com',
        'password': '12345678'
    })
    assert response.status_code == 201
    assert 'id' in response.json

def test_login_user(client):
    client.post('/api/users/register', json={
        'full_name': 'Tester User',
        'email': 'tester@mail.com',
        'password': '12345678'
    })
    response = client.post('/api/users/login', json={
        'email': 'tester@mail.com',
        'password': '12345678'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json