from pydantic import Field
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class UserBook(Base):
    __tablename__ = "users_books"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"), primary_key=True)
    
    # borrowed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # returned_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)  # مثلاً 1 تا 5
    user: Mapped[list["User"]] = relationship("User", back_populates="user_books")
    book: Mapped[list["Book"]] = relationship("Book", back_populates="user_books")
