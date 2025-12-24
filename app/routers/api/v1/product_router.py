from fastapi import APIRouter, Depends
from app.dependencies import get_db
from app.schemas.product_schemas import Product, ProductDisplay
from sqlalchemy.orm.session import Session
from app.services import product_service
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/products', tags=['products'])

@router.post('/new', response_model=Product)
def create_product(product: Product, db: Session = Depends(get_db)):
    return product_service.create_product(product, db)

@router.get('', response_model=ProductDisplay)
async def get_products(product_id: int, db: AsyncSession = Depends(get_db)):
    products = await product_service.get_product(product_id, db)
    return products