import requests

from app.domain.factory.users import create_dummy_user_data


def test_user_factory(user_management_system_url):
    status = []

    for n in range(100):
        data = create_dummy_user_data()
        response = requests.post(f"{user_management_system_url}/user", json=data)

        status.append(response.status_code == 200)

    assert all(status)
