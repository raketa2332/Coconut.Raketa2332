
from api.api_manager import ApiManager
from entities.user import User
from models.base_models import RegisterUserResponse
from utils.data_generator import DataGenerator


class TestAuthAPI:
    def test_registration_user(self, api_manager: ApiManager, registration_user_data):
        response = api_manager.auth_api.register_user(user_data=registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data=login_data)
        response_data = response.json()

        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_auth_user_with_invalid_creds(self, api_manager: ApiManager, registered_user):

        login_data_with_invalid_passwd = {
            "email": registered_user["email"],
            "password": DataGenerator.generate_random_password(),
        }
        response = api_manager.auth_api.login_user(login_data=login_data_with_invalid_passwd, expected_status=401)
        response_data = response.json()

        assert "accessToken" not in response_data, "В ответе присутствует токен аутентификации"
        assert "error" in response_data, "В ответе отсутствует сообщение об ошибке"
        assert response_data["error"] == "Unauthorized", "Текст ошибки не совпадает"

        login_data_with_invalid_email = {
            "email": DataGenerator.generate_random_email(),
            "password": registered_user["password"],
        }
        response = api_manager.auth_api.login_user(login_data=login_data_with_invalid_email, expected_status=401)
        response_data = response.json()
        assert "accessToken" not in response.json(), "В ответе присутствует Access Токен"
        assert "error" in response.json(), "Отсутствует сообщение об ошибке"
        assert response.json()["error"] == "Unauthorized", "Текст ошибки не совпадает"

        response = api_manager.auth_api.login_user(login_data={}, expected_status=401)
        response_data = response.json()
        assert "accessToken" not in response.json(), "В ответе присутствует Access Токен"
        assert "error" in response.json(), "Отсутствует сообщение об ошибке"
        assert response.json()["error"] == "Unauthorized", "Текст ошибки не совпадает"
