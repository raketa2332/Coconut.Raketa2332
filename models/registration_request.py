from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator
from constants.roles import Roles


class RegistrationRequest(BaseModel):
    email: EmailStr = Field(...)
    full_name: str = Field(..., min_length=2, max_length=100, alias='fullName')
    password: str = Field(..., min_length=8, max_length=64)
    password_repeat: str = Field(..., alias='passwordRepeat')
    roles: List[Roles] = Field(...)
    verified: Optional[bool] = Field(None)
    banned: Optional[bool] = Field(None)

    @model_validator(mode="after")
    def check_password_match(self):
        if self.password != self.password_repeat:
            raise ValidationError("Passwords don't match")
        return self

    class Config:
        populate_by_name = True