from sqlalchemy import Column, String, ForeignKey
from app.database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(50), nullable=False)
