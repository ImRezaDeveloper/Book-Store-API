from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from app.schemas.product_schemas import Product, ProductDisplay
from sqlalchemy.orm.session import Session
from app.services import product_service
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/products', tags=['products'])

@router.post('/new', response_model=Product)
async def create_product(product: Product, db: AsyncSession = Depends(get_db)):
    return await product_service.create_product(product, db)

@router.get('/by-id')
async def get_products(product_id: int, db: AsyncSession = Depends(get_db)):
    products = await product_service.get_product(product_id, db)
    return products

@router.get('')
async def get_products(db: AsyncSession = Depends(get_db)):
    products = await product_service.get_all_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="db is empty!")
    return products