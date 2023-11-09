from fastapi import HTTPException
from schemas import BaseModel
from typing import List, Type, TypeVar, Generic
from database import Base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseDBModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[BaseDBModel]):
        self.model = model

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

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
