import pytest

from faker import Faker
from fastapi.testclient import TestClient

from app import get_app, get_user_management_v1, get_travels_match_network_v1


@pytest.fixture(scope="module")
def client():
    with TestClient(get_app()) as client:
        yield client


@pytest.fixture(scope="module")
def client_user_management():
    with TestClient(get_user_management_v1()) as client:
        yield client


@pytest.fixture(scope="module")
def client_travels_match_network():
    with TestClient(get_travels_match_network_v1()) as client:
        yield client


@pytest.fixture(scope="session")
def fake():
    Faker.seed(0)

    return Faker('es_MX')
