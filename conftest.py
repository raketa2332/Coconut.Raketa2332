import random

import pytest
import requests
from faker import Faker

from api.api_manager import ApiManager
from constant import BASE_URL, HEADERS, LOGIN_ENDPOINT, REGISTER_ENDPOINT, SUPER_ADMIN_LOGIN, SUPER_ADMIN_PASSWORD
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator


faker = Faker()


@pytest.fixture()
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"],
    }


@pytest.fixture()
def registered_user(requester, test_user):
    response = requester.send_request(method="POST", endpoint=REGISTER_ENDPOINT, data=test_user, expected_status=201)
    response_data = response.json()
    register_user = test_user.copy()
    register_user["id"] = response_data["id"]
    return register_user


@pytest.fixture()
def requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture()
def auth_session(test_user):
    register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    response = requests.post(url=register_url, json=test_user, headers=HEADERS)
    assert response.status_code == 201, "Ошибка рeгистрации"

    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {"email": test_user["email"], "password": test_user["password"]}
    response = requests.post(url=login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"

    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


@pytest.fixture()
def test_genre():
    return {"name": DataGenerator.generate_random_genre()}


@pytest.fixture()
def random_genre(api_manager):
    response = api_manager.movie_api.get_genres_list()
    response_data = response.json()
    return random.choice(response_data)


@pytest.fixture()
def locations():
    return ["MSK", "SPB"]


@pytest.fixture()
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


@pytest.fixture()
def test_movie(admin_api_manager, test_movie_data):
    response = admin_api_manager.movie_api.create_movie(test_movie_data)
    response_data = response.json()
    assert "id" in response_data, "id фильма отсутствует"
    assert response_data.get("name") == test_movie_data["name"], "Название фильма не совпадает"
    assert response_data.get("genreId") == test_movie_data["genreId"], "id жанра не совпадает"
    return response_data


@pytest.fixture(scope="class")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="class")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="class")
def admin_api_manager(api_manager):
    api_manager.auth_api.authenticate((SUPER_ADMIN_LOGIN, SUPER_ADMIN_PASSWORD))
    return api_manager
