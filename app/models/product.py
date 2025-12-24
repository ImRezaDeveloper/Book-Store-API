from app.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Float, ForeignKey, Integer, String, Column
# from .author import Author
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock = Column(Integer)
    rating_avg = Column(Float, default=0)
    rating_count = Column(Integer, default=0)

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")