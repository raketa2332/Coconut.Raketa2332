from pydantic import BaseModel
from constants.roles import Roles


class RegistrationUserDTO(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list < Roles.value > Roles
