from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from app.models.product import Book
from .associations import user_book


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="User")
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # رابطه many-to-many با کتاب‌ها
    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary=user_book,             # ← مهم
        back_populates="users"
    )
    # orders = relationship("Order", back_populates="user")
    # comments = relationship("Comment", back_populates="user")
