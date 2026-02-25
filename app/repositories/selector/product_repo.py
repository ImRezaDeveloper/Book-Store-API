from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models.product import Book
from app.schemas.product_schemas import ProductDisplay, ProductUpdate

async def get_product_by_id(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Book).filter_by(id=id)
    result = await db.execute(stmt)
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found with this id"
        )
        
    return book
        
async def get_all_products(db: AsyncSession = Depends(get_db)):
    products = select(Book)
    result = await db.execute(products)
    final = result.scalars().all()
    # mappings for dict
    if not final:
        raise HTTPException(
            status_code=404,
            detail="There is no product"
        )
        
    return final

async def update_product(
    product_id: int,
    request: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Book).where(Book.id == product_id)
    )
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = request.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    for key, value in update_data.items():
        setattr(book, key, value)

    await db.commit()
    await db.refresh(book)

    return book

async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = select(Book).where(Book.id == product_id)
    result = await db.execute(product)
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Product not found with this id")

    await db.delete(book)
    await db.commit()
    return Response("product successfully deleted!", status_code=201)