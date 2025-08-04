from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, Boolean

Base = declarative_base()


class UserDBModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(String)

class MovieDBModel(Base):
    __tablename__ = "movies"
