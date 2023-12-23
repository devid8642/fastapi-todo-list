from backend.schemas import UserPublic


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


def test_update_user(client, user):
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


def test_delete_user(client, user):
    success_response = client.delete('/users/1/delete/')
    fail_response = client.delete('/users/1/delete/')

    assert success_response.status_code == 200
    assert success_response.json() == {
        'detail': 'User deleted',
    }

    assert fail_response.status_code == 404
    assert fail_response.json() == {
        'detail': 'User not found',
    }


def test_get_token(client, user):
    success_response = client.post(
        '/token/',
        data={
            'username': user.email,
            'password': user.plain_password,
        },
    )
    fail_response = client.post(
        '/token/',
        data={
            'username': 'teste',
            'password': 'teste',
        },
    )
    token = success_response.json()

    assert success_response.status_code == 200
    assert 'acess_token' in token
    assert 'token_type' in token

    assert fail_response.status_code == 400
    assert fail_response.json() == {'detail': 'Incorrect email or password'}
