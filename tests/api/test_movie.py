from api.api_manager import ApiManager
from constant import SUPER_ADMIN_LOGIN, SUPER_ADMIN_PASSWORD
import random

class TestGenresAPI:
    def test_create_genre(self, admin_api_manager: ApiManager, test_genre):

        response = admin_api_manager.movie_api.create_genre(test_genre)
        response_data = response.json()
        assert "id" in response_data, "Отсутствует id жанра в ответе"
        genre_id = response_data["id"]
        assert response_data.get("name") == test_genre["name"], "Название жанра отличается"

        response = admin_api_manager.movie_api.get_genre(genre_id)
        response_data = response.json()
        assert response_data.get("id") == genre_id, "Отличается id жанра"
        assert response_data.get("name") ==test_genre["name"]

    def test_delete_genre(self, admin_api_manager: ApiManager, test_genre):

        response = admin_api_manager.movie_api.create_genre(test_genre)
        genre_id = response.json().get("id")

        response = admin_api_manager.movie_api.delete_genre(genre_id)
        response_data = response.json()
        assert response_data.get("id") == genre_id, "Отличаются id жанра"
        assert response_data.get("name") == test_genre["name"], "Название жанра отличается"

        response = admin_api_manager.movie_api.get_genre(genre_id, expected_status=404)
        response_data = response.json()
        assert response_data.get("message") == "Жанр не найден", "Отличается message в теле ответа"
        assert response_data.get("error") == "Not Found", "Отличается сообщение ошибки"
        assert response_data.get("statusCode") == 404, "Отличается статус код в теле ответа"

    def test_get_genres_list(self, api_manager):
        response = api_manager.movie_api.get_genres_list()
        response_data = response.json()
        assert "id" in random.choice(response_data), "Отсутствует id жанра"
        assert "name" in random.choice(response_data), "Отсутствует название жанра"

    def test_cant_create_genre_with_empty_name(self, admin_api_manager):
        response = admin_api_manager.movie_api.create_genre({"name": " "}, expected_status=400)
        response_data = response.json()
        assert "message" in response_data, "Отсутствует поле message"
        assert "Поле name должно содержать не менее 3 символов" in response_data["message"], "Отсутствует сообщение об ошибке"
        assert "Поле name не может содержать пробелы в начале или в конце" in response_data["message"], "Отсутствует сообщение об ошибке"
        assert response_data.get("error") == "Bad Request", "Расшифровка статус кода не совпадает"
        assert response_data.get("statusCode") == 400, "Статус код в теле ответа не совпадает"

    def test_cant_create_genre_with_name_less_than_3_characters(self, admin_api_manager):
        response = admin_api_manager.movie_api.create_genre({"name": "ff"}, expected_status=400)
        response_data = response.json()
        assert "message" in response_data, "Отсутствует поле message"
        assert "Поле name должно содержать не менее 3 символов" in response_data["message"], " Отсутствует сообщение об ошибке"
        assert response_data.get("error") == "Bad Request", "Расшифровка статус кода не совпадает"
        assert response_data.get("statusCode") == 400, "Статус код в теле ответа не совпадает"

    def test_cant_create_genre_if_name_already_exists (self, admin_api_manager, test_genre):
        response = admin_api_manager.movie_api.create_genre(test_genre)
        response_data = response.json()
        assert "id" in response_data, "Отсутствует id жанра"
        assert "name" in response_data, "Отсутствует название жанра"

        response = admin_api_manager.movie_api.create_genre(test_genre,expected_status=409)
        response_data = response.json()
        assert response_data.get("message") == "Такой жанр уже существует", "Сообщение об ошибке не совпадает"
        assert response_data.get("error") == "Conflict", "Расшифровка статус кода не совпадает"
        assert response_data.get("statusCode") == 409, "Статус код в теле не совпадает"



