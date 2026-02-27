from fastapi import Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models.associations import UserBook
from app.models.user import User
from sqlalchemy.orm import selectinload
from app.schemas.user_schemas import UserUpdate
from app.security.auth.dependencies import get_current_user
from app.security.auth.hashing import hash_pwd

async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = select(User).where(User.is_deleted == False).options(selectinload(User.books))
    result = await db.execute(users)
    final = result.scalars().all()
    
    return final

async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = select(User).where(User.id == user_id, User.is_deleted == False).options(selectinload(User.books))
    result = await db.execute(user)
    final = result.scalar_one_or_none()
    
    return final

async def update_user(request: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    update_data = request.model_dump(exclude_unset=True, exclude_none=True)
    
    if "password" in update_data:
        current_user.password = hash_pwd(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(current_user, key, value)
        
    await db.commit()
    await db.refresh(current_user)
    return current_user

async def delete_user_by_admin(user_id: int, db: AsyncSession = Depends(get_db)):
    user = select(User).filter(User.id == user_id)
    result = await db.execute(user)
    final = result.scalars().first()        
    
    await db.delete(final)
    await db.commit()
        
    return Response('user was deleted successfully')

async def get_user_products(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    products = select(UserBook).where(UserBook.user_id == current_user.id).options(selectinload(UserBook.book))
    result = await db.execute(products)
    final = result.scalars().all()
    
    UserBook.user_id = current_user.id
    
    return {
        "products": final
    }
