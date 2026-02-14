from sqlalchemy import Column, Integer, ForeignKey, Table
from db.base import Base

user_book = Table(
    "user_books",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    # added_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # status   = Column(String(20), default="reading")
)