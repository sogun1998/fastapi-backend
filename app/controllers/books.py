# app/controllers/books.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.services import books as book_service
from app.database import get_db

router = APIRouter(prefix="/books")

# --------------------------
# POST /books
# --------------------------
@router.post("", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
  book, author = book_service.create_book(db, book)
  return schemas.Book(
    id=book.id,
    title=book.title,
    author_id=book.author_id,
    author_name=author.name if author else None
  )

# --------------------------
# GET /books
# --------------------------
@router.get("", response_model=list[schemas.Book])
def list_books(db: Session = Depends(get_db)):
  books = book_service.get_books(db)
  return [schemas.Book(
    id=book.id,
    title=book.title,
    author_id=book.author_id,
    author_name=book.author.name if book.author else None
  ) for book in books]


# --------------------------
# GET /books/{book_id}
# --------------------------
@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: str, db: Session = Depends(get_db)):
  book = book_service.get_book(db, book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  return schemas.Book(
    id=book.id,
    title=book.title,
    author_id=book.author_id,
    author_name=book.author.name if book.author else None
  )


# --------------------------
# DELETE /books/{book_id}
# --------------------------
@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(book_id: str, db: Session = Depends(get_db)):
  book, author = book_service.delete_book(db, book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  return schemas.Book(
    id=book.id,
    title=book.title,
    author_id=book.author_id,
    author_name=author.name if author else None
  )
