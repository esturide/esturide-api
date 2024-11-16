from fastapi.testclient import TestClient

from app.presentation.api import root

client = TestClient(root)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
