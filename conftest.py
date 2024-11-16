import pytest
import requests


@pytest.fixture(scope='session', autouse=True)
def hello_world():
    return 'Hello World!'


@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    def is_responsive(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except ConnectionError:
            return False

    port = docker_services.port_for("httpbin", 8000)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )

    return url


@pytest.fixture(scope='session', autouse=True)
def default_url():
    return "http://localhost:8000"


@pytest.fixture(scope='session', autouse=True)
def user_management_system_url(default_url):
    return f"{default_url}/user_management_system"
