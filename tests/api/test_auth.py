import pytest
import requests

from api.api_manager import ApiManager
from constant import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import DataGenerator


class TestAuthAPI:
    def test_registration_user(self, api_manager: ApiManager, test_user):
        """
        Тест регистрации пользователя
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data=login_data,expected_status=200)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_auth_user_with_invalid_creds(self,api_manager:ApiManager, registered_user):

        #Попытка логина с невалидным паролем
        login_data_with_invalid_passwd = {
            "email": registered_user["email"],
            "password": DataGenerator.generate_random_password()
        }
        response = api_manager.auth_api.login_user(login_data=login_data_with_invalid_passwd,expected_status=401)
        response_data = response.json()
        assert "accessToken" not in response_data, "В ответе присутствует токен аутентификации"
        assert "error" in response_data, "В ответе отсутствует сообщение об ошибке"
        assert response_data["error"] == "Unauthorized", "Текст ошибки не совпадает"

        #Попытка логина с невалидным логином
        login_data_with_invalid_email = {
            "email" : DataGenerator.generate_random_email(),
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data=login_data_with_invalid_email, expected_status=401)
        response_data = response.json()
        assert "accessToken" not in response.json(), "В ответе присутствует Access Токен"
        assert "error" in response.json(), "Отсутствует сообщение об ошибке"
        assert response.json()["error"] == "Unauthorized", "Текст ошибки не совпадает"

        #Попытка логина с пустым телом
        response = api_manager.auth_api.login_user(login_data={},expected_status=401)
        response_data = response.json()
        assert "accessToken" not in response.json(), "В ответе присутствует Access Токен"
        assert "error" in response.json(), "Отсутствует сообщение об ошибке"
        assert response.json()["error"] == "Unauthorized", "Текст ошибки не совпадает"