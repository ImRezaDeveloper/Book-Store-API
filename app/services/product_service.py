from fastapi import Depends, HTTPException, Response
from sqlalchemy import delete, insert, update
from app.dependencies import get_db
from app.models.product import Book
from app.schemas.product_schemas import Product, ProductDisplay, ProductUpdate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.security.auth.dependencies import require_admin
from app.repositories.selector import product_repo

async def create_product(request: Product, db: AsyncSession) -> Book:
    new_book = Book(
        title=request.title,
        description=request.description,
        price=request.price,
        stock=request.stock,
        rating_avg=request.rating_avg,
        rating_count=request.rating_count,
        author_id=request.author_id
    )
    
    db.add(new_book)
    await db.commit()        
    await db.refresh(new_book)  

    return new_book

async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    product = await product_repo.get_product_by_id(id=id, db=db)
    return product

async def get_all_products(db: AsyncSession = Depends(get_db)):
    products = await product_repo.get_all_products(db=db)
    return products

async def update_product(request: ProductUpdate, product_id: int, db: AsyncSession):
    product = await product_repo.update_product(request=request, product_id=product_id, db=db)
    return product

async def delete_product(product_id: int, db: AsyncSession):
    product = await product_repo.delete_product(product_id=product_id, db=db)
    return product