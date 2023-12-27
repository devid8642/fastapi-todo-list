from backend.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/create/',
        json={
            'username': 'devid',
            'email': 'devid@example.com',
            'password': 'secret',
        },
    )
    fail_response = client.post(
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

    assert fail_response.status_code == 400
    assert fail_response.json() == {
        'detail': 'User already registered',
    }


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    success_response = client.get(f'/users/{user.id}/')
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


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}/update/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
        headers={
            'Authorization': f'Bearer {token}',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_update_a_different_user(client, token):
    response = client.put(
        '/users/2/update/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
        headers={
            'Authorization': f'Bearer {token}',
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Not enough permissions',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}/delete/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {
        'detail': 'User deleted',
    }


def test_delete_a_different_user(client, token):
    response = client.delete(
        '/users/2/delete/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Not enough permissions',
    }
