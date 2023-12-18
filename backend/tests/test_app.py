def test_root_returned_200_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/create/',
        json={
            'username': 'devid',
            'email': 'devid@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'username': 'devid',
        'email': 'devid@example.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {
        'users': [{'id': 1, 'username': 'devid', 'email': 'devid@example.com'}]
    }


def test_read_user(client):
    success_response = client.get('/users/1/')
    fail_response = client.get('/users/2/')

    assert success_response.status_code == 200
    assert success_response.json() == {
        'id': 1,
        'username': 'devid',
        'email': 'devid@example.com',
    }
    assert fail_response.status_code == 404
    assert fail_response.json() == {
        'detail': 'User not found',
    }


def test_update_user(client):
    success_response = client.put(
        '/users/1/update/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    fail_response = client.put(
        '/users/2/update/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert success_response.status_code == 200
    assert success_response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }

    assert fail_response.status_code == 404
    assert fail_response.json() == {'detail': 'User not found'}
