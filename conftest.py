import random

import pytest
import requests
from faker import Faker

from api.api_manager import ApiManager
from constants.constant import BASE_URL, HEADERS, LOGIN_ENDPOINT, REGISTER_ENDPOINT, SUPER_ADMIN_LOGIN, SUPER_ADMIN_PASSWORD
from constants.roles import Roles
from custom_requester.custom_requester import CustomRequester
from entities.user import User
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator


faker = Faker()


@pytest.fixture(scope="function")
def test_user():
    def _test_user():
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        return {
            "email": random_email,
            "fullName": random_name,
            "password": random_password,
            "passwordRepeat": random_password,
            "roles": [Roles.USER.value],
        }
    return _test_user


@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    data = test_user()
    response = requester.send_request(method="POST", endpoint=REGISTER_ENDPOINT, data=data, expected_status=201)
    response_data = response.json()
    register_user = data.copy()
    register_user["id"] = response_data["id"]
    return register_user


@pytest.fixture(scope="function")
def requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="function")
def auth_session(test_user):
    register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    response = requests.post(url=register_url, json=test_user(), headers=HEADERS)
    assert response.status_code == 201, "Ошибка рeгистрации"

    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {"email": test_user()["email"], "password": test_user()["password"]}
    response = requests.post(url=login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"

    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


@pytest.fixture(scope="function")
def test_genre():
    return {"name": DataGenerator.generate_random_genre()}


@pytest.fixture(scope="function")
def random_genre(api_manager):
    response = api_manager.movie_api.get_genres_list()
    response_data = response.json()
    return random.choice(response_data)


@pytest.fixture(scope="function")
def locations():
    return ["MSK", "SPB"]


@pytest.fixture(scope="function")
def test_movie_data(random_genre, locations):
    return {
        "name": DataGenerator.generate_random_movie_title(),
        "imageUrl": "https://example.com/image.png",
        "price": faker.random_int(min=1, max=10000),
        "description": DataGenerator.generate_random_movie_description(),
        "location": random.choice(locations),
        "published": faker.boolean(),
        "genreId": random_genre.get("id"),
    }


@pytest.fixture(scope="function")
def test_movie(super_admin: User, test_movie_data: dict) -> dict:
    response = super_admin.api.movie_api.create_movie(test_movie_data)
    response_data = response.json()

    assert "id" in response_data, "id фильма отсутствует"
    assert response_data.get("name") == test_movie_data["name"], "Название фильма не совпадает"
    assert response_data.get("genreId") == test_movie_data["genreId"], "id жанра не совпадает"
    return response_data


@pytest.fixture(scope="function")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="function")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="function")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture(scope="function")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    update_data = test_user().copy()
    update_data.update({
        "verified": True,
        "banned": False
    })
    return update_data


@pytest.fixture(scope="function")
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture(scope="function")
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session
    )

    response = super_admin.api.user_api.create_user(creation_user_data).json()
    user_id = response["id"]
    super_admin.api.user_api.update_user(user_id=user_id, data={"roles": [Roles.ADMIN.value]})
    admin.api.auth_api.authenticate(admin.creds)
    return admin
