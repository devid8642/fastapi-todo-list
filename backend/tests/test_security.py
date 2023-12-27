from jose import jwt

from backend.security import create_access_token, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    encoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert encoded['test'] == 'test'
    assert encoded['exp']
