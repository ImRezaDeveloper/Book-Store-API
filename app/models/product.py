from app.db.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Float, ForeignKey, Integer, String, Column

from .associations import UserBook

class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)
    rating_avg: Mapped[float] = mapped_column(Float, default=0)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)
    
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship("Author", back_populates="books")
    
    user_books: Mapped[list["UserBook"]] = relationship(
            "UserBook",
            back_populates="book"
        )
    
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="users_books",
        back_populates="books",
        viewonly=True
    )