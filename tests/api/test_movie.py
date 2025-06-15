import math
import random

from api.api_manager import ApiManager
from utils.data_generator import DataGenerator


class TestGenreAPI:
    def test_create_genre(self, admin_api_manager: ApiManager, test_genre):
        response = admin_api_manager.movie_api.create_genre(test_genre)
        response_data = response.json()
        assert response_data.get("id"), "id не может быть None или отсутствовать вовсе"
        genre_id = response_data["id"]
        assert response_data.get("name") == test_genre["name"]

        response = admin_api_manager.movie_api.get_genre(genre_id)
        response_data = response.json()
        assert response_data.get("id") == genre_id
        assert response_data.get("name") == test_genre["name"]

    def test_delete_genre(self, admin_api_manager: ApiManager, test_genre):
        response = admin_api_manager.movie_api.create_genre(test_genre)
        genre_id = response.json().get("id")

        response = admin_api_manager.movie_api.delete_genre(genre_id)
        response_data = response.json()
        assert response_data.get("id") == genre_id
        assert response_data.get("name") == test_genre["name"]

        response = admin_api_manager.movie_api.get_genre(genre_id, expected_status=404)
        response_data = response.json()
        assert response_data.get("message") == "Жанр не найден"
        assert response_data.get("error") == "Not Found"
        assert response_data.get("statusCode") == 404

    def test_get_genres_list(self, admin_api_manager: ApiManager):
        response = admin_api_manager.movie_api.get_genres_list()
        response_data = response.json()
        assert "id" in random.choice(response_data), "Отсутствует id жанра"
        assert "name" in random.choice(response_data), "Отсутствует название жанра"

    def test_cant_create_genre_with_empty_name(self, admin_api_manager: ApiManager):
        response = admin_api_manager.movie_api.create_genre({"name": " "}, expected_status=400)
        response_data = response.json()

        assert response_data.get("message"), "message не может быть пустым или отсутствовать"
        assert "Поле name должно содержать не менее 3 символов" in response_data["message"]
        assert "Поле name не может содержать пробелы в начале или в конце" in response_data["message"]
        assert response_data.get("error") == "Bad Request"
        assert response_data.get("statusCode") == 400

    def test_cant_create_genre_with_name_less_than_3_characters(self, admin_api_manager: ApiManager):
        response = admin_api_manager.movie_api.create_genre({"name": "ff"}, expected_status=400)
        response_data = response.json()

        assert response_data.get("message"), "message не может быть пустым или отсутствовать"
        assert "Поле name должно содержать не менее 3 символов" in response_data["message"]
        assert response_data.get("error") == "Bad Request"
        assert response_data.get("statusCode") == 400

    def test_cant_create_genre_if_name_already_exists(self, admin_api_manager: ApiManager, test_genre):
        response = admin_api_manager.movie_api.create_genre(test_genre)
        response_data = response.json()
        assert response_data.get("id"), "id не может быть None или отсутствовать"
        assert response_data.get("name"), "name не может быть None|Пустым или отсутствовать"

        response = admin_api_manager.movie_api.create_genre(test_genre, expected_status=409)
        response_data = response.json()
        assert response_data.get("message") == "Такой жанр уже существует"
        assert response_data.get("error") == "Conflict"
        assert response_data.get("statusCode") == 409


class TestMovieAPI:
    def test_create_movie(self, admin_api_manager: ApiManager, test_movie_data):
        response = admin_api_manager.movie_api.create_movie(test_movie_data)
        response_data = response.json()

        response = admin_api_manager.movie_api.get_genre(test_movie_data["genreId"])
        genre_data = response.json()

        assert response_data.get("id"), "id не может быть None или отсутствовать"
        movie_id = response_data["id"]
        assert response_data.get("name") == test_movie_data["name"]
        assert response_data.get("price") == test_movie_data["price"]
        assert response_data.get("description") == test_movie_data["description"]
        assert response_data.get("imageUrl") == test_movie_data["imageUrl"]
        assert response_data.get("location") == test_movie_data["location"]
        assert response_data.get("published") == test_movie_data["published"]
        assert response_data.get("genreId") == test_movie_data["genreId"]
        assert response_data.get("genre").get("name") == genre_data["name"]
        assert response_data.get("createdAt"), "createdAt не может быть пустым или отсутствовать"
        assert "rating" in response_data

        response = admin_api_manager.movie_api.get_movie(movie_id)
        response_data = response.json()
        assert response_data.get("id") == movie_id
        assert response_data.get("name") == test_movie_data["name"]
        assert response_data.get("genreId") == test_movie_data["genreId"]

    def test_edit_movie(self, admin_api_manager: ApiManager, test_movie_data, random_genre):
        response = admin_api_manager.movie_api.create_movie(test_movie_data)
        response_data = response.json()
        assert response_data.get("id"), "id не может быть None или отсутствовать"
        movie_id = response_data["id"]
        assert response_data.get("name") == test_movie_data["name"]
        assert response_data.get("genreId") == test_movie_data["genreId"]

        new_data = {
            "name": DataGenerator.generate_random_movie_title(),
            "genreId": random_genre["id"],
            "price": random.randint(1, 10000),
        }

        response = admin_api_manager.movie_api.edit_movie(movie_id, new_data)
        new_response_data = response.json()
        assert new_response_data.get("id") == movie_id
        assert new_response_data.get("name") == new_data["name"]
        assert new_response_data.get("genreId") == new_data["genreId"]
        assert new_response_data.get("price") == new_data["price"]

        assert new_response_data.get("location") == response_data.get("location")
        assert new_response_data.get("published") == response_data.get("published")

    def test_get_movies_list(self, admin_api_manager: ApiManager):
        response = admin_api_manager.movie_api.get_movie_list()
        response_data = response.json()
        assert response_data.get("count"), "count не может быть None или отсутствовать"
        assert response_data.get("page") == 1, "page по умолчанию должен быть равен 1"
        assert response_data.get("pageSize") == 10, "pageSize по умолчанию должен быть равен 10"
        assert response_data.get("pageCount") == math.ceil(
            response_data.get("count") / response_data.get("pageSize")
        ), "Общее кол-во страниц не совпадает"
        assert "movies" in response_data, "movies отсутствует в ответе"

        any_movie = random.choice(response_data["movies"])
        assert any_movie.get("id"), "id не может быть None или отсутствовать"
        assert any_movie.get("name"), "name не может быть пустым или отсутствовать"
        assert any_movie.get("genreId"), "genreId не может быть None или отсутствовать"
        assert "published" in any_movie
        assert any_movie.get("location"), "location не может быть пустым или отсутствовать"

    def test_get_movies_list_with_page_size_and_location_filter(self, admin_api_manager: ApiManager, locations):
        location = random.choice(locations)
        page_size = random.randint(5, 15)

        response = admin_api_manager.movie_api.get_movie_list(pageSize=page_size, locations=location)
        response_data = response.json()
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data.get("pageSize") == page_size, "Кол-во фильмов на странице не совпадает"
        assert response_data.get("pageCount") == math.ceil(
            response_data.get("count") / response_data.get("pageSize")
        ), "Общее кол-во страниц не совпадает"

        movies = response_data.get("movies")
        for movie in movies:
            assert movie.get("location") == location

    def test_delete_movie(self, admin_api_manager: ApiManager, test_movie):
        response = admin_api_manager.movie_api.delete_movie(test_movie["id"])
        response_data = response.json()

        assert response_data.get("id") == test_movie["id"]
        assert response_data.get("name") == test_movie["name"]
        assert response_data.get("genreId") == test_movie["genreId"]

        response = admin_api_manager.movie_api.get_movie(test_movie["id"], expected_status=404)
        response_data = response.json()
        assert response_data.get("message") == "Фильм не найден"

    def test_cant_create_movie_without_name(self, admin_api_manager: ApiManager, test_movie_data):
        del test_movie_data["name"]
        response = admin_api_manager.movie_api.create_movie(movie_data=test_movie_data, expected_status=400)
        response_data = response.json()
        assert response_data.get('message'), "message должен быть в теле ответа и не может быть пустым"
        assert "Поле name должно содержать не менее 3 символов" in response_data["message"]
        assert "Поле name должно быть строкой" in response_data["message"]
        assert "Поле name не может быть пустым" in response_data["message"]
        assert response_data.get("error") == "Bad Request"
        assert response_data.get("statusCode") == 400

    def test_cant_delete_non_exists_movie(self, admin_api_manager: ApiManager):
        response = admin_api_manager.movie_api.delete_movie(movie_id=123456789, expected_status=404)
        response_data = response.json()
        assert response_data.get("message") == "Фильм не найден"
        assert response_data.get("error") == "Not Found"
        assert response_data.get("statusCode") == 404

    def test_cant_get_delete_movie(self, admin_api_manager: ApiManager, test_movie):
        response = admin_api_manager.movie_api.delete_movie(test_movie["id"])
        response_data = response.json()
        assert response_data.get("id") == test_movie["id"]
        assert response_data.get("name") == test_movie["name"]

        response = admin_api_manager.movie_api.get_movie(test_movie["id"], expected_status=404)
        response_data = response.json()
        assert response_data.get("message") == "Фильм не найден"
        assert response_data.get("error") == "Not Found"
        assert response_data.get("statusCode") == 404
