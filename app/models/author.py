from app.db.base import Base
from sqlalchemy import Integer, String, Column
# from .product import Book
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.product import Book

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    bio = Column(String, nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")
        