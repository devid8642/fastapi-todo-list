from jose import jwt

from backend.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    encoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    assert encoded['test'] == 'test'
    assert encoded['exp']
