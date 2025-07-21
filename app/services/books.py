import uuid
from sqlalchemy.orm import Session
from app import schemas
from app.models import books, authors
from sqlalchemy.orm import joinedload

# ----------------
# BOOK
# ----------------
def create_book(db: Session, book: schemas.BookCreate):
  # Check author exists
  author = db.query(authors.Author).filter(authors.Author.id == book.author_id).first()
  if not author:
      return None

  db_book = books.Book(id=str(uuid.uuid4()), title=book.title, author_id=book.author_id)
  db.add(db_book)
  db.commit()
  db.refresh(db_book)
  return db_book, author


def get_books(db: Session):
  return db.query(books.Book).options(joinedload(books.Book.author)).all()

def get_book(db: Session, book_id: str):
  return db.query(books.Book).filter(books.Book.id == book_id).options(joinedload(books.Book.author)).first()
  

def delete_book(db: Session, book_id: str):
  book = get_book(db, book_id)
  if book:
      db.delete(book)
      db.commit()
      return book, book.author
  return None, None
