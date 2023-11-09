from database import Base

from sqlalchemy import Column, Integer, String


class BaseDBModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)


class BookDB(BaseDBModel):
    __tablename__ = "books"
    title = Column(String, index=True)
    author = Column(String)


class UserDB(BaseDBModel):
    __tablename__ = "users"
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
