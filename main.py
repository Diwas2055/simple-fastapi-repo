# main.py
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core import BaseRepository
from custom_middleware import ExceptionMiddleware
from database import get_db
from exception_handler import custom_validation_exception_handler
from logger_info import logger
from models import BookDB, UserDB
from schemas import Book, User

app = FastAPI()
app.exception_handler(RequestValidationError)(custom_validation_exception_handler)
app.exception_handler(HTTPException)(http_exception_handler)
app.add_middleware(ExceptionMiddleware)

book_repository = BaseRepository(BookDB)
user_repository = BaseRepository(UserDB)


@app.get("/health-checker", status_code=200)
async def check_health():
    logger.info("Server is running")
    return 5 / 0
    return JSONResponse(status_code=200, content={"message": "Server is running"})


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


@app.post("/process_request")
async def process_request(request: Request):
    # Check Content-Type
    content_type = request.headers.get("Content-Type")

    if not content_type or "application/json" not in content_type:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

    # Get the request body as a UTF-8 string
    try:
        body_bytes = await request.body()
        if body_bytes:
            body_text = body_bytes.decode("utf-8")
        else:
            body_text = body_bytes
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid UTF-8 encoding")

    print("body_text", body_text)

    return {"message": "Request processed successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        port=8001,
    )
