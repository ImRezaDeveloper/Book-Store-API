from typing import List
from fastapi import APIRouter, Depends, Request
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.cart_service import CartService
from app.schemas.author_schemas import Authors, AuthorDisplay

router = APIRouter(tags=['cart'], prefix='/cart')

@router.get('', status_code=200)
async def get_cart(request: Request):
    cart_service = CartService(request)
    
    cart = await cart_service.get_cart()
    
    if cart is None or cart == {}:
        return {"items": {}, "message": "سبد خرید خالی است"}
    
    return {"cart": cart}

@router.get('/author/{id}', status_code=200, response_model=AuthorDisplay)
async def get_author_id(author_id: int, db: AsyncSession = Depends(get_db)):
    return await author_service.get_author_by_id(author_id, db)

@router.post('/new', status_code=201, response_model=Authors)
async def create_author(author: Authors, db: AsyncSession = Depends(get_db)):
    return await author_service.create_author(author, db)

@router.put('/update', status_code=200)
async def update_author(author_id: int, request: Authors, db: AsyncSession = Depends(get_db)):
    updated_author = await author_service.update_author(author_id, request, db)
    return updated_author

@router.delete('/delete', status_code=201)
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    return await author_service.delete_author(author_id, db)