from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': user.email,
            'password': user.plain_password,
        },
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_inexistent_user(client):
    response = client.post(
        '/auth/token/',
        data={'username': 'test@example.com', 'password': 'test'},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_incorrect_password(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': user.email,
            'password': 'wrong password',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_expires(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token/',
            data={
                'username': user.email,
                'password': user.plain_password,
            },
        )

        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}/update/',
            json={
                'username': 'test',
                'email': 'test@example.com',
                'password': 'testeeste',
            },
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, user, token):
    response = client.post(
        '/auth/refresh_token/',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token/',
            data={
                'username': user.email,
                'password': user.plain_password,
            },
        )

        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token/',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}
