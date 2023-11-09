from typing import Generic, List, Type, TypeVar

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()

ModelType = TypeVar("ModelType", bound=BaseModel)


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


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[BaseDBModel]):
        self.model = model

    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def get_by_id(self, db: Session, id: int) -> ModelType:
        item = db.query(self.model).filter(self.model.id == id).first()
        if item:
            return item
        raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")

    def create(self, db: Session, item: ModelType) -> ModelType:
        db_item = self.model(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def update(self, db: Session, id: int, item: ModelType) -> ModelType:
        db_item = db.query(self.model).filter(self.model.id == id).first()
        if db_item:
            for key, value in item.model_dump().items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return db_item
        raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")

    def delete(self, db: Session, id: int) -> None:
        db_item = db.query(self.model).filter(self.model.id == id).first()
        if db_item:
            db.delete(db_item)
            db.commit()
        else:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found"
            )


book_repository = BaseRepository(BookDB)
user_repository = BaseRepository(UserDB)


class Book(BaseModel):
    id: int
    title: str
    author: str


class User(BaseModel):
    id: int
    username: str
    email: str


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


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    return book_repository.get_all(db=db)


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return book_repository.get_by_id(id=book_id, db=db)


@app.post("/books", response_model=Book)
def create_book(book: Book, db: Session = Depends(get_db)):
    return book_repository.create(item=book, db=db)


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    return book_repository.update(id=book_id, item=book, db=db)


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_repository.delete(id=book_id, db=db)


@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    return user_repository.get_all(db=db)


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_repository.get_by_id(id=user_id, db=db)


@app.post("/users", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    return user_repository.create(item=user, db=db)


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    return user_repository.update(id=user_id, item=user, db=db)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_repository.delete(db=db, id=user_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8001)
