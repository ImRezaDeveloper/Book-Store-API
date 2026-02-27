from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import insert, select
from app.dependencies import get_db
from app.models.associations import UserBook
from app.schemas.user_schemas import UserRegister, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import User, Book
from app.security.auth.hashing import hash_pwd
from app.security.auth.dependencies import check_login_user, check_exist_book, get_current_user, require_admin, soft_delete_user
from enum import Enum
from app.repositories.selector import user_repo
app = FastAPI()

async def get_users(db: AsyncSession = Depends(get_db)):
    users = await user_repo.get_all_users(db=db)
    if not users:
        raise HTTPException(status_code=404, detail="there are not users in db!")
    
    return users

async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_repo.get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="the user not found with this id!")

    return user

async def create_user(user: UserRegister, db = Depends(get_db)) -> User:
    new_user = User(
        username = user.username,
        email = user.email,
        password = hash_pwd(user.password),
        role = user.role
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(request: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_update = await user_repo.update_user(request=request, current_user=current_user, db=db)
    return user_update


async def delete_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = await soft_delete_user(db, current_user)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "user was soft deleted successfully"}


# user_product operations

async def add_product_to_user(product_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = await check_exist_book(product_id=product_id, db=db)
    
    if current_user in product.users:
        raise HTTPException(
            status_code=400,
            detail="Product already assigned to this user"
        )
        
    stmt = insert(UserBook).values(
        user_id = current_user.id,
        book_id = product.id
    )
    
    await db.execute(stmt)
    await db.commit()
    await db.refresh(product, attribute_names=["users"])
    
    return {
            "message": "product added to user successfully",
            "user_id": current_user.id,
            "product_id": product.id
        }
    
    
async def get_user_products(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_products = await user_repo.get_user_products(current_user=current_user, db=db)
    
    if not user_products:
        raise HTTPException(
            status_code=400,
            detail="you don't have any product in your cart"
        )
    return user_products

async def get_me(current_user: User):
    return current_user
