from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from app.models.product import Book
from .associations import UserBook


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="User")
    is_active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  
    
    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary="users_books",
        back_populates="users",
        viewonly=True
    )
    
    user_books: Mapped[list["UserBook"]] = relationship(
        "UserBook",
        back_populates="user",
        cascade="all, delete-orphan"   # اختیاری
    )
    # orders = relationship("Order", back_populates="user")
    # comments = relationship("Comment", back_populates="user")
