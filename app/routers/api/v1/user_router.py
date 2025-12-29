from typing import List
from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import user_service
from app.schemas.user_schemas import UserDisplay, GetUser

router = APIRouter(tags=['users'], prefix='/users')

@router.get('', status_code=200, response_model=List[UserDisplay])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_service.get_users(db)

@router.get('/user/{id}', status_code=200, response_model=UserDisplay)
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_service.get_user_by_id(user_id, db)

@router.post('/new', status_code=201, response_model=GetUser)
async def create_user(user: GetUser, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(user, db)

@router.put('/update', status_code=200)
async def update_user(user_id: int, request: GetUser, db: AsyncSession = Depends(get_db)):
    updated_user = await user_service.update_user(user_id, request, db)
    return updated_user

@router.delete('/delete', status_code=201)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_service.delete_user(user_id, db)