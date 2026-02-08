from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select
from app.dependencies import get_db
from app.schemas.user_schemas import GetUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import User, Book
from app.security.auth.hashing import hash_pwd
from app.security.auth.dependencies import check_login_user, check_exist_book, check_user, get_current_user
from enum import Enum

app = FastAPI()

async def get_users(db = Depends(get_db)):
    users = select(User).options(selectinload(User.books))
    result = await db.execute(users)
    final = result.scalars().all()
    if not final:
        raise HTTPException(
            status_code=404,
            detail="DB is empty!"
        )
    return final

async def get_user_by_id(user_id: int, db = Depends(get_db)):
    user = select(User).where(User.id == user_id).options(selectinload(User.books))
    result = await db.execute(user)
    final = result.scalars().first()
    
    if not final:
        raise HTTPException(status_code=404, detail="the user not found with this id!")

    return final

async def create_user(user: GetUser, db = Depends(get_db)) -> User:
    new_user = User(
        username = user.username,
        email = user.email,
        password = hash_pwd(user.password)
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(user_id: int, request: GetUser, db: AsyncSession = Depends(get_db)):
    user = await check_user(user_id=user_id, db=db)
    
    updated_user = request.model_dump(exclude_unset=True)
    
    for key, value in updated_user.items():
        setattr(user, key, value)
        
    await db.commit()
    await db.refresh(user)
    
    return user

async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await check_user(user_id=user_id, db=db)
        
    await db.delete(user)
    await db.commit()
        
    return Response('user was deleted successfully')

# user_product operations

async def add_product_to_user(product_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    product = await check_exist_book(product_id=product_id, db=db)
    user = await check_user(user_id=user_id, db=db)
    
    product.user_id = user.id
    
    if product.user_id == user.id:
        raise HTTPException(
            status_code=400,
            detail="Product already assigned to this user"
        )
    
    await db.commit()
    await db.refresh(product)
    
    return {
            "message": "product added to user successfully",
            "user_id": user.id,
            "product_id": product.id
        }
    
async def get_user_products(user: User):
    return user.books