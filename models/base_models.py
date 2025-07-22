from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator

from constants.roles import Roles


class TestUser(BaseModel):
    email: EmailStr = Field(...)
    full_name: str = Field(..., min_length=2, max_length=100, alias='fullName')
    password: str = Field(..., min_length=8, max_length=64)
    password_repeat: str = Field(..., alias='passwordRepeat')
    roles: list[Roles] = Field(default=Roles.USER)
    verified: Optional[bool] = Field(None)
    banned: Optional[bool] = Field(None)

    @model_validator(mode="after")
    def check_password_match(self):
        if self.password != self.password_repeat:
            raise ValueError("Passwords don't match")
        return self

    class Config:
        populate_by_name = True

        json_encoders = {
            Roles: lambda v: v.value
        }

class RegisterUserResponse(BaseModel):
    id: str = Field(...)
    email: EmailStr = Field(...)
    full_name: str = Field(..., alias="fullName")
    verified: bool = Field(...)
    banned: bool = Field(...)
    roles: List[Roles] = Field(...)
    created_at: Optional[str] = Field(None)

    @field_validator("created_at")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Invalid creation date")
        return value