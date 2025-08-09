from faker import Faker
from fastapi.testclient import TestClient

from test.factories.user import create_user


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_user_management(client: TestClient, fake: Faker):
    response = client.get("/v1/user-management")

    assert response.status_code == 200


def test_register_user(client_user_management: TestClient, fake: Faker):
    data = create_user(fake)
    response = client_user_management.post("/user", json=data)

    assert response.status_code == 200
