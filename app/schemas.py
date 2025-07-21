from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AuthorCreate(BaseModel):
  name: str = Field(..., max_length=50)


class Author(BaseModel):
  id: str
  name: str
  model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
  title: str = Field(..., max_length=100)
  author_id: str

class Book(BaseModel):
  id: str
  title: str
  author_id: str
  author_name: Optional[str] = None
  model_config = ConfigDict(from_attributes=True)
