from fastapi import APIRouter, Depends
from app.dependencies import get_db
from app.schemas.product_schemas import Product, ProductDisplay
from sqlalchemy.orm.session import Session
from app.services import product_service

router = APIRouter(prefix='products', tags=['products'])

@router.post('/new', response_model=Product)
def create_product(product: Product, db: Session = Depends(get_db)):
    return product_service.create_product(product=product, get_db=db)

@router.get('', response_model=ProductDisplay)
def get_products(id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db=db, id=id)