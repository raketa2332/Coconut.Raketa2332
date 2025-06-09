import requests

from api.api_manager import ApiManager
from constant import BASE_URL, HEADERS, LOGIN_ENDPOINT, REGISTER_ENDPOINT
import pytest
from faker import Faker
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester

faker = Faker()

@pytest.fixture(scope='function')
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope='function')
def registered_user(requester, test_user):
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    register_user = test_user.copy()
    register_user["id"] = response_data["id"]
    return register_user


@pytest.fixture(scope='function')
def requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope='function')
def auth_session(test_user):
    register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    response = requests.post(url=register_url, json=test_user, headers=HEADERS)
    assert response.status_code == 201, "Ошибка рeгистрации"

    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {
        "email": test_user['email'],
        "password": test_user['password']
    }
    response = requests.post(url=login_url,json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"

    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope='session')
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

