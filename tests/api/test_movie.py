from api.api_manager import ApiManager
from constant import SUPER_ADMIN_LOGIN, SUPER_ADMIN_PASSWORD
import random

class TestMoviesApi:
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