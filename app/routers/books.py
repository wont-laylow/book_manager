from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from app.models import Book
 
router = APIRouter(prefix = "/books", tags=["Books"])

@router.post("/", response_model=schemas.ResponseBook)
async def create_book(book: schemas.CreateBook, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())

    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
    except Exception as e:
        db.rollback()
        print("commit failed:", e)
    
    try: 
        return new_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[schemas.ResponseBook])
async def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    
    return books


@router.get("/{book_id}", response_model=schemas.ResponseBook)
async def get_book_by_id(book_id : int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code = 404, detail="Book not found")
    
    return book


@router.put("/{book_id}", response_model=schemas.ResponseBook)
async def update_book(book_id : int, book_data: schemas.CreateBook, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book_data.dict().items():
        setattr(book, key, value)

    try:
        db.commit()
        db.refresh(book)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update")
    
    return book


@router.delete("/{book_id}", response_model=schemas.ResponseBook)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Not found")
    
    try:
        db.delete(book)
        db.commit()
        return book
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Commit failed") 

    


        
    
