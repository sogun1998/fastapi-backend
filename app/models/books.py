from sqlalchemy import Column, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    author_id = Column(String(36), ForeignKey("authors.id"))
    author = relationship("Author", backref="books")
