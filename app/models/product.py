from app.db.base import Base
from sqlalchemy import Float, ForeignKey, Integer, String, Column

class Book(Base):
    __tablename__ = "Book"
    Id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock = Column(Integer)  # تعداد موجود
    author_id = Column(Integer, ForeignKey("authors.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    rating_avg = Column(Float, default=0)
    rating_count = Column(Integer, default=0)