import math
import random
from http.client import responses
from platform import uname_result

import pytest
import requests
from api.api_manager import ApiManager
from conftest import common_user, super_admin
from entities.user import User
from utils.data_generator import DataGenerator


class TestGenreAPI:
    def test_create_genre(self, super_admin: User, test_genre):
        response = super_admin.api.movie_api.create_genre(test_genre)
        response_data = response.json()
        assert response_data.get("id"), "id не может быть None или отсутствовать вовсе"
        genre_id = response_data["id"]
        assert response_data.get("name") == test_genre["name"]

        response = super_admin.api.movie_api.get_genre(genre_id)
        response_data = response.json()
        assert response_data.get("id") == genre_id
        assert response_data.get("name") == test_genre["name"]

    def test_delete_genre(self, super_admin: User, test_genre: dict):
        response = super_admin.api.movie_api.create_genre(test_genre)
        genre_id = response.json().get("id")

        response = super_admin.api.movie_api.delete_genre(genre_id).json()
        assert response.get("id") == genre_id
        assert response.get("name") == test_genre["name"]

        response = super_admin.api.movie_api.get_genre(genre_id, expected_status=404).json()
        assert response.get("message") == "Жанр не найден"
        assert response.get("error") == "Not Found"

    def test_get_genres_list(self, super_admin: User):
        response = super_admin.api.movie_api.get_genres_list()
        response_data = response.json()
        assert "id" in random.choice(response_data), "Отсутствует id жанра"
        assert "name" in random.choice(response_data), "Отсутствует название жанра"

    def test_cant_create_genre_with_empty_name(self, super_admin: User):
        response = super_admin.api.movie_api.create_genre({"name": " "}, expected_status=400)
        response_data = response.json()

        assert response_data.get("message"), "message не может быть пустым или отсутствовать"
        assert "Поле name должно содержать не менее 3 символов" in response_data["message"]
        assert "Поле name не может содержать пробелы в начале или в конце" in response_data["message"]
        assert response_data.get("error") == "Bad Request"
        assert response_data.get("statusCode") == 400

    def test_cant_create_genre_with_name_less_than_3_characters(self, super_admin: User):
        response = super_admin.api.movie_api.create_genre({"name": "ff"}, expected_status=400)
        response_data = response.json()

        assert response_data.get("message"), "message не может быть пустым или отсутствовать"
        assert "Поле name должно содержать не менее 3 символов" in response_data["message"]
        assert response_data.get("error") == "Bad Request"
        assert response_data.get("statusCode") == 400

    def test_cant_create_genre_if_name_already_exists(self, super_admin: User, test_genre):
        response = super_admin.api.movie_api.create_genre(test_genre)
        response_data = response.json()
        assert response_data.get("id"), "id не может быть None или отсутствовать"
        assert response_data.get("name"), "name не может быть None|Пустым или отсутствовать"

        response = super_admin.api.movie_api.create_genre(test_genre, expected_status=409)
        response_data = response.json()
        assert response_data.get("message") == "Такой жанр уже существует"
        assert response_data.get("error") == "Conflict"
        assert response_data.get("statusCode") == 409


class TestMovieAPI:

    def test_create_movie(self, super_admin: User, test_movie_data):
        response = super_admin.api.movie_api.create_movie(test_movie_data)
        response_data = response.json()

        response = super_admin.api.movie_api.get_genre(test_movie_data["genreId"])
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

        response = super_admin.api.movie_api.get_movie(movie_id)
        response_data = response.json()
        assert response_data.get("id") == movie_id
        assert response_data.get("name") == test_movie_data["name"]
        assert response_data.get("genreId") == test_movie_data["genreId"]

    def test_edit_movie(self, super_admin: User, test_movie_data, random_genre):
        response = super_admin.api.movie_api.create_movie(test_movie_data)
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

        response = super_admin.api.movie_api.edit_movie(movie_id, new_data)
        new_response_data = response.json()
        assert new_response_data.get("id") == movie_id
        assert new_response_data.get("name") == new_data["name"]
        assert new_response_data.get("genreId") == new_data["genreId"]
        assert new_response_data.get("price") == new_data["price"]

        assert new_response_data.get("location") == response_data.get("location")
        assert new_response_data.get("published") == response_data.get("published")

    def test_get_movies_list(self, super_admin: User):
        response = super_admin.api.movie_api.get_movie_list()
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

    def test_get_movies_list_with_page_size_and_location_filter(self, super_admin: User, locations):
        location = random.choice(locations)
        page_size = random.randint(5, 15)

        response = super_admin.api.movie_api.get_movie_list(pageSize=page_size, locations=location)
        response_data = response.json()
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data.get("pageSize") == page_size, "Кол-во фильмов на странице не совпадает"
        assert response_data.get("pageCount") == math.ceil(
            response_data.get("count") / response_data.get("pageSize")
        ), "Общее кол-во страниц не совпадает"

        movies = response_data.get("movies")
        for movie in movies:
            assert movie.get("location") == location

    @pytest.mark.flaky(reruns=2, rerun_delay=1)
    @pytest.mark.parametrize("role_name,expected_status", [
        pytest.param("common_user", 403),
        pytest.param("admin", 403, marks=pytest.mark.xfail(reason="Известный баг")),
        pytest.param("super_admin", 200)
    ])
    def test_delete_movie(self, request, role_name, expected_status, test_movie):
        role: User = request.getfixturevalue(role_name)

        response = role.api.movie_api.delete_movie(test_movie["id"], expected_status=expected_status).json()
        if expected_status == 200:
            assert response.get("id") == test_movie["id"]
            assert response.get("name") == test_movie["name"]
            assert response.get("genreId") == test_movie["genreId"]

            response = role.api.movie_api.get_movie(test_movie["id"], expected_status=404)
        elif expected_status == 403:
            pass

    @pytest.mark.flaky(reruns=2, rerun_delay=1)
    def test_cant_create_movie_without_name(self, super_admin: User, test_movie_data):
        del test_movie_data["name"]
        response = super_admin.api.movie_api.create_movie(movie_data=test_movie_data, expected_status=400)
        response_data = response.json()
        assert response_data.get('message'), "message должен быть в теле ответа и не может быть пустым"
        assert "Поле name должно содержать не менее 3 символов" in response_data["message"]
        assert "Поле name должно быть строкой" in response_data["message"]
        assert "Поле name не может быть пустым" in response_data["message"]
        assert response_data.get("error") == "Bad Request"
        assert response_data.get("statusCode") == 400

    def test_cant_delete_non_exists_movie(self, super_admin: User):
        response = super_admin.api.movie_api.delete_movie(movie_id=123456789, expected_status=404)
        response_data = response.json()
        assert response_data.get("message") == "Фильм не найден"
        assert response_data.get("error") == "Not Found"
        assert response_data.get("statusCode") == 404

    def test_cant_get_delete_movie(self, super_admin: User, test_movie: dict):
        response = super_admin.api.movie_api.delete_movie(test_movie["id"])
        response_data = response.json()
        assert response_data.get("id") == test_movie["id"]
        assert response_data.get("name") == test_movie["name"]

        response = super_admin.api.movie_api.get_movie(test_movie["id"], expected_status=404)
        response_data = response.json()
        assert response_data.get("message") == "Фильм не найден"
        assert response_data.get("error") == "Not Found"
        assert response_data.get("statusCode") == 404
    
    @pytest.mark.slow
    def test_common_user_cant_create_movie(self, common_user: User, test_movie_data: dict):
        response = common_user.api.movie_api.create_movie(test_movie_data, expected_status=403).json()

        assert response.get("message") == "Forbidden resource"
        assert response.get("error") == "Forbidden"
        assert response.get("statusCode") == 403

    @pytest.mark.slow
    @pytest.mark.parametrize("min_price,max_price,location,genre_id", [
        (100, 200, "SPB", 1),
        (100, 200, "MSK", 1),
        (201, 300, "SPB", 2),
        (201, 300, "MSK", 2)
    ])
    def test_get_movies_list_with_filters(self, min_price, max_price, location, genre_id, common_user):
        response_movies = (
            common_user.api.movie_api.get_movie_list(
                minPrice=min_price, maxPrice=max_price, locations=location, genreId=genre_id
            )
            .json()
            .get("movies")
        )

        for movie in response_movies:
            price = movie.get("price")
            assert (price >= min_price) and (price <= max_price), "Стоимость фильма не попадает в допустимый диапазон"
            assert movie.get("location") == location
            assert movie.get("genreId") == genre_id
