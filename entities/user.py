from pydantic import EmailStr

from api.api_manager import ApiManager


class User:
    def __init__(self, email: EmailStr, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self):
        return self.email, self.password
