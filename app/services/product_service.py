from fastapi import Depends, HTTPException
from app.dependencies import get_db
from app.models.product import Book
from sqlalchemy.orm.session import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

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

async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Book).filter_by(Id=id)
    result = await db.execute(stmt)
    book = result.scalars().first()  # scalars() برای گرفتن مدل‌ها
    return book