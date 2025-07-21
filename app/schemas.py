from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AuthorCreate(BaseModel):
  name: str = Field(..., max_length=50)


class Author(BaseModel):
  id: str
  name: str
  model_config = ConfigDict(from_attributes=True)
