from _pydatetime import datetime

from pydantic import BaseModel, Field, model_validator, EmailStr
from typing import Optional

class Movie(BaseModel):
    name: str = Field(..., min_length=1)
    price: int = Field(..., ge=1, le=10000)
    location: str
    genre_id: int = Field(..., alias="genreId")

    @model_validator(mode = "before")
    def check_allow_location(self):
        cities = ["MSK", "SPB"]
        if self.location not in  cities:
            raise ValueError(f"Invalid location: {self.location}")
        return self

movie = Movie(name="Test", price=100, location="MSK", genreId=1)
print(movie.model_dump(by_alias=True))