# repositories.py
from typing import List, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from core import BaseRepository
from schemas import Book, User

ModelType = TypeVar("ModelType", bound=BaseModel)


class BookRepository(BaseRepository[Book]):
    def get_all(self, db: Session) -> List[Book]:
        return super().get_all(db)

    def get_by_id(self, db: Session, id: int) -> Book:
        return super().get_by_id(db, id)

    def create(self, db: Session, item: Book) -> Book:
        return super().create(db, item)

    def update(self, db: Session, id: int, item: Book) -> Book:
        return super().update(db, id, item)

    def delete(self, db: Session, id: int) -> None:
        super().delete(db, id)


class UserRepository(BaseRepository[User]):
    def get_all(self, db: Session) -> List[User]:
        return super().get_all(db)

    def get_by_id(self, db: Session, id: int) -> User:
        return super().get_by_id(db, id)

    def create(self, db: Session, item: User) -> User:
        return super().create(db, item)

    def update(self, db: Session, id: int, item: User) -> User:
        return super().update(db, id, item)

    def delete(self, db: Session, id: int) -> None:
        super().delete(db, id)
