import uuid
from sqlalchemy.orm import Session
from app import schemas
from app.models import authors

# ----------------
# AUTHOR
# ----------------
def create_author(db: Session, author: schemas.AuthorCreate):
  db_author = authors.Author(id=str(uuid.uuid4()), name=author.name)
  db.add(db_author)
  db.commit()
  db.refresh(db_author)
  return db_author
