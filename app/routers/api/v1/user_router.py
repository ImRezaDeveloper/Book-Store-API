from typing import List
from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services import user_service
from app.schemas.user_schemas import UserDisplay, UserUpdate, UserRegister
from app.schemas.product_schemas import ProductUserDisplay
from app.security.auth import dependencies

router = APIRouter(tags=['users'], prefix='/users')

@router.get("", status_code=200, response_model=List[UserDisplay])
async def get_all_users(db: AsyncSession = Depends(get_db), admin: bool = Depends(dependencies.require_admin)):
    return await user_service.get_users(db=db)
    

@router.get('/user/{id}', status_code=200, response_model=UserDisplay)
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db), admin: bool = Depends(dependencies.require_admin), current_user: User = Depends(dependencies.get_current_active_user)):
    return await user_service.get_user_by_id(user_id, db)

@router.post('/new', status_code=201, response_model=UserRegister)
async def create_user(user: UserRegister, db: AsyncSession = Depends(get_db), admin: bool = Depends(dependencies.require_admin), current_user: User = Depends(dependencies.get_current_user)):
    return await user_service.create_user(user, db)

@router.patch('/update', status_code=200)
async def update_user(
    user: UserUpdate,
    current_user: User = Depends(dependencies.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await user_service.update_user(user, current_user, db)

@router.delete('/delete', status_code=204)
async def delete_user(db: AsyncSession = Depends(get_db),current_user: User = Depends(dependencies.get_current_active_user)):
    return await user_service.delete_user(db, current_user)

@router.delete('/delete/{user_id}', status_code=204)
async def delete_user_admin(user_id: int, db: AsyncSession = Depends(get_db), admin: bool = Depends(dependencies.require_admin), current_user: User = Depends(dependencies.get_current_user)):
    return await user_service.delete_user_by_admin(user_id, db)

@router.post('/products', status_code=201)
async def create_product_user(product_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(dependencies.get_current_user)):
    return await user_service.add_product_to_user(product_id, db, current_user)

@router.get("/me/products", status_code=200)
async def get_user_products(current_user: User = Depends(dependencies.get_current_user), db: AsyncSession = Depends(get_db)):
    products = await user_service.get_user_products(current_user, db)
    return products

@router.get("/me")
async def get_user(
    current_user: User = Depends(dependencies.get_current_user)
):
    return await user_service.get_me(current_user)
