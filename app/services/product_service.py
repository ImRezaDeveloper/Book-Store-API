from fastapi import Depends, HTTPException, Response
from sqlalchemy import delete, insert, update
from app.dependencies import get_db
from app.models.product import Book
from app.schemas.product_schemas import Product, ProductDisplay
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

async def update_product(request: ProductDisplay, product_id: int, db: AsyncSession):
    product = select(Book).where(Book.id == product_id)
    result = await db.execute(product)
    book = result.scalars().first()  
    
    if not book:
        raise HTTPException(status_code=404, detail="Product not found with this id")
    
    update_data = request.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(book, key, value)
    
    await db.commit()
    
    await db.refresh(book)
    
    return book

async def delete_product(product_id: int, db: AsyncSession):
    product = select(Book).where(Book.id == product_id)
    result = await db.execute(product)
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Product not found with this id")

    await db.delete(book)
    await db.commit()
    return Response("product successfully deleted!", status_code=201)