# app/controllers/authors.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, services
from app.services import authors as author_service
from app.database import get_db

router = APIRouter(prefix="/authors")

# --------------------------
# POST /authors
# --------------------------
@router.post("", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return author_service.create_author(db, author)
