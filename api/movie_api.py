from constant import BASE_API_URL, GENRE_ENDPOINT, MOVIE_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class MovieAPI(CustomRequester):
    def __init__(self, session, base_url=BASE_API_URL):
        super().__init__(session=session, base_url=base_url)

    def create_genre(self, genre_name, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=GENRE_ENDPOINT,
            expected_status=expected_status,
            data=genre_name
        )

    def delete_genre(self, genre_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{GENRE_ENDPOINT}/{genre_id}",
            expected_status=expected_status
        )

    def get_genre(self, genre_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{GENRE_ENDPOINT}/{genre_id}",
            expected_status=expected_status)

    def get_genres_list(self, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=GENRE_ENDPOINT,
            expected_status=expected_status)

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            expected_status=expected_status,
            data=movie_data
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
        )

    def get_movie_list(self, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            expected_status=expected_status,
            params=kwargs)

    def edit_movie(self, movie_id, new_movie_data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
            data=new_movie_data,
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )
