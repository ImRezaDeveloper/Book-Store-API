from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    
    books = relationship("Book", back_populates="user")
    # orders = relationship("Order", back_populates="user")
    # comments = relationship("Comment", back_populates="user")
