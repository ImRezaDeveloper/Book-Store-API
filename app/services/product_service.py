from fastapi import Depends, HTTPException
from sqlalchemy import delete, insert
from app.dependencies import get_db
from app.models.product import Book
from app.schemas.product_schemas import Product
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_product(request: Product, db: AsyncSession) -> Book:
    new_book = Book(
        title=request.title,
        description=request.description,
        price=request.price,
        stock=request.stock,
        rating_avg=request.rating_avg,
        rating_count=request.rating_count,
    )
    
    db.add(new_book)
    await db.commit()        # await اضافه کن
    await db.refresh(new_book)  # await اضافه کن
    
    return new_book

async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Book).filter_by(id=id)
    result = await db.execute(stmt)
    book = result.scalars().first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found with this id"  # بهتره string باشه یا dict با ساختار مشخص
        )
    return book

async def get_all_products(db: AsyncSession = Depends(get_db)):
    products = select(Book)
    result = await db.execute(products)
    product = result.scalars().all()
    return product