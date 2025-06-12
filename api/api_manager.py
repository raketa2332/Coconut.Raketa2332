import requests

from api.auth_api import AuthAPI
from api.movie_api import MovieAPI
from api.user_api import UserAPI
from constant import SUPER_ADMIN_LOGIN, SUPER_ADMIN_PASSWORD


class ApiManager:
    def __init__(self, session: requests.Session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movie_api = MovieAPI(session)

    def login_as_super_admin(self):
        self.auth_api.authenticate((SUPER_ADMIN_LOGIN, SUPER_ADMIN_PASSWORD))