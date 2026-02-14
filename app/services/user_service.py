from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select
from app.dependencies import get_db
from app.schemas.user_schemas import UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import User, Book
from app.security.auth.hashing import hash_pwd
from app.security.auth.dependencies import check_login_user, check_exist_book, get_current_user
from enum import Enum

app = FastAPI()

async def get_users(db: AsyncSession = Depends(get_db)):
    users = select(User).options(selectinload(User.books))
    result = await db.execute(users)
    final = result.scalars().all()
    if not final:
        raise HTTPException(
            status_code=404,
            detail="DB is empty!"
        )
    return final

async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = select(User).where(User.id == user_id).options(selectinload(User.books))
    result = await db.execute(user)
    final = result.scalars().first()
    
    if not final:
        raise HTTPException(status_code=404, detail="the user not found with this id!")

    return final

async def create_user(user: UserUpdate, db = Depends(get_db)) -> User:
    new_user = User(
        username = user.username,
        email = user.email,
        password = hash_pwd(user.password)
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(request: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    update_data = request.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        current_user.password = hash_pwd(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(current_user, key, value)
        
    await db.commit()
    await db.refresh(current_user)
    return current_user

async def delete_user(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await current_user
    
    if not user:
        return {
            "error": "you don't have permission to delete users"
        }
        
    await db.delete(user)
    await db.commit()
        
    return Response('user was deleted successfully')

# user_product operations

async def add_product_to_user(product_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = await check_exist_book(product_id=product_id, db=db)
    
    if product.user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Product already assigned to this user"
        )
        
    product.user_id = current_user.id
        
    # await db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return {
            "message": "product added to user successfully",
            "user_id": current_user.id,
            "product_id": product.id
        }
    
async def get_user_products(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    products = select(Book).filter(Book.id == current_user.id)
    result = await db.execute(products)
    final = result.scalars().all()
    
    if not final:
        raise HTTPException(
            status_code=400,
            detail="you don't have any product in your cart"
        )
        
    products.user_id = current_user.id
    
    return {
        "products": final
    }

async def get_me(current_user: User):
    return current_user
