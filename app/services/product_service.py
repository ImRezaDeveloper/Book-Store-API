from fastapi import Depends, HTTPException
from app.dependencies import get_db
from app.models.product import Book
from sqlalchemy.orm.session import Session

def create_product(db: Session, request: Book):
    new_product = Book(
        Id = request.Id,
        title = request.title,
        description = request.description,
        price = request.price,
        stock = request.stock,
        rating_avg = request.rating_avg,
        rating_count = request.rating_count
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_product(db: Session, id: int):
    product = db.query(Book).filter(Book.Id == id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail={"product not found with this id"})
    
    return product