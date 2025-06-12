import math
from multiprocessing.context import assert_spawning
from unittest import defaultTestLoader

from api.api_manager import ApiManager
from constant import SUPER_ADMIN_LOGIN, SUPER_ADMIN_PASSWORD
import random

from utils.data_generator import DataGenerator


class TestGenreAPI:
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

    def test_get_genres_list(self, admin_api_manager):
        response = admin_api_manager.movie_api.get_genres_list()
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

class TestMovieAPI:

    def test_create_movie(self, admin_api_manager, test_movie_data):
        response = admin_api_manager.movie_api.create_movie(test_movie_data)
        response_data = response.json()

        response = admin_api_manager.movie_api.get_genre(test_movie_data["genreId"])
        genre_data = response.json()

        assert "id" in response_data, "Отсутствует id фильма"
        movie_id = response_data["id"]
        assert response_data.get("name") == test_movie_data["name"], "Название фильма не совпадает"
        assert response_data.get("price") == test_movie_data["price"], "Цена фильма не совпадает"
        assert response_data.get("description") == test_movie_data["description"], "Описание фильма не совпадает"
        assert response_data.get("imageUrl") == test_movie_data["imageUrl"], "URL изображения не совпадет"
        assert response_data.get("location") == test_movie_data["location"], "Локация не совпадает"
        assert response_data.get("published") == test_movie_data["published"], "Статус публикации не совпадает"
        assert response_data.get("genreId") == test_movie_data["genreId"], "id жанра не совпадает"
        assert response_data.get("genre").get("name") == genre_data["name"], "Название жанра не совпадает"
        assert "createdAt" in response_data, "Отсутствует дата создания"
        assert "rating" in response_data

        response = admin_api_manager.movie_api.get_movie(movie_id)
        response_data = response.json()
        assert response_data.get("id") == movie_id, "id фильма не совпадет"
        assert response_data.get("name") == test_movie_data["name"], "Название фильма не совпадает"
        assert response_data.get("genreId") == test_movie_data["genreId"], "Название жанра не совпадает"

    def test_edit_movie(self, admin_api_manager, test_movie_data, random_genre):

        response = admin_api_manager.movie_api.create_movie(test_movie_data)
        response_data = response.json()
        assert "id" in response_data, "Отсутствует id фильма"
        movie_id = response_data["id"]
        assert response_data.get("name") == test_movie_data["name"], "Название фильма не совпадает"
        assert response_data.get("genreId") == test_movie_data["genreId"], "id жанра не совпадает"

        new_data = {
            "name": DataGenerator.generate_random_movie_title(),
            "genreId": random_genre["id"],
            "price": random.randint(1,10000)
        }

        response = admin_api_manager.movie_api.edit_movie(movie_id, new_data)
        new_response_data = response.json()
        assert new_response_data.get("id") == movie_id, "id фильма не совпадает"
        assert new_response_data.get("name") == new_data["name"], "Название фильма не совпадает"
        assert new_response_data.get("genreId") == new_data["genreId"], "id жанра не совпадает"
        assert new_response_data.get("price") == new_data["price"], "Цена фильма не совпадает"

        assert new_response_data.get("location") == response_data.get("location"), "Локация фильма изменилась"
        assert new_response_data.get("published") == response_data.get("published"), "Статус публикации не совпадает"

    def test_get_movies_list(self, admin_api_manager):
        response = admin_api_manager.movie_api.get_movie_list()
        response_data = response.json()
        assert "count" in response_data, "count отсутствует в ответе"
        assert response_data.get("page") == 1, "Некорректная страница в ответе"
        assert response_data.get("pageSize") == 10, "Кол-во фильмов на одной странице не совпадает"
        assert response_data.get("pageCount") == math.ceil(response_data.get("count") / response_data.get("pageSize")), "Общее кол-во страниц не совпадает"
        assert "movies" in response_data, "movies отсутствует в ответе"

        any_movie = random.choice(response_data["movies"])
        assert "id" in any_movie, "Отсутствует id фильма"
        assert "name" in any_movie, "Отсутствует название фильма"
        assert "genreId" in any_movie, "Отсутствует id жанра"
        assert "published" in any_movie, "Отсутствует статус публикации у фильма"
        assert "location" in any_movie, "Отсутствует локация фильма"

    def test_get_movies_list_with_pageSize_and_location_filter(self, admin_api_manager, locations):
        location = random.choice(locations)
        page_size = random.randint(5,15)

        response = admin_api_manager.movie_api.get_movie_list(pageSize=page_size, locations=location)
        response_data = response.json()
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data.get("pageSize") == page_size, "Кол-во фильмов на странице не совпадает"
        assert response_data.get("pageCount") == math.ceil(response_data.get("count") / response_data.get("pageSize")), "Общее кол-во страниц не совпадает"

        movies = response_data.get("movies")
        for movie in movies:
            assert movie.get("location") == location, "Локация фильма не совпадает"

    def test_delete_movie(self, admin_api_manager, test_movie):
        response = admin_api_manager.movie_api.delete_movie(test_movie["id"])
        response_data = response.json()

        assert response_data.get("id") == test_movie["id"], "id фильма не совпадает"
        assert response_data.get("name") == test_movie["name"], "Название фильма не совпадает"
        assert response_data.get("genreId") == test_movie["genreId"], "id жанра не совпадает"

        response = admin_api_manager.movie_api.get_movie(test_movie["id"], expected_status=404)
        response_data = response.json()
        assert response_data.get("message") == "Фильм не найден", "Сообщение ошибки не совпадает"

