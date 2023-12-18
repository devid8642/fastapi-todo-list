from fastapi.testclient import TestClient

from backend.app import app


def test_root_returned_200_and_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}
