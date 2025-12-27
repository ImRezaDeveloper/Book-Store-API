from app.db.base import Base
from sqlalchemy import Integer, String, Column
# from .product import Book
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    bio = Column(String, nullable=True)

    books = relationship("Book", back_populates="author")
