# main.py
from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import get_db
from mail import send_email
from schemas import Book, User
from core import BaseRepository
from models import BookDB, UserDB

app = FastAPI()

book_repository = BaseRepository(BookDB)
user_repository = BaseRepository(UserDB)


@app.get("/", status_code=200)
async def home():
    data_obj = {"title": "Hello World", "name": "John Doe"}
    await send_email(template_name="v2/demo.html", data_obj=data_obj)
    return {"message": "Hello World"}


@app.get("/books", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return book_repository.get_all(db=db, skip=skip, limit=limit)


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
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_repository.get_all(db=db, skip=skip, limit=limit)


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
