from fastapi.testclient import TestClient

from app.presentation.api import root
from app.presentation.api.user_management_system import user_management_system

client = TestClient(root)
user_client = TestClient(user_management_system)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
