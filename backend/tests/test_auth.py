def test_get_token(client, user):
    success_response = client.post(
        '/auth/token/',
        data={
            'username': user.email,
            'password': user.plain_password,
        },
    )
    fail_response = client.post(
        '/auth/token/',
        data={
            'username': 'teste',
            'password': 'teste',
        },
    )
    token = success_response.json()

    assert success_response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token

    assert fail_response.status_code == 400
    assert fail_response.json() == {'detail': 'Incorrect email or password'}
