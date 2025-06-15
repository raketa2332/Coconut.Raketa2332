import os

from dotenv import load_dotenv


load_dotenv()

BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
BASE_API_URL = "https://api.dev-cinescope.coconutqa.ru"

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
GENRE_ENDPOINT = "/genres"
MOVIE_ENDPOINT = "/movies"

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

SUPER_ADMIN_LOGIN = os.environ["SUPER_ADMIN_LOGIN"]
SUPER_ADMIN_PASSWORD = os.environ["SUPER_ADMIN_PASSWORD"]
