
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import select
from app.security.auth.jwt_handler import verify_token
from app.security.auth.oauth2 import oauth_schemes
from app.dependencies import get_db
from app.models.user import User
from app.models.product import Book
from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user(token: Annotated[str, Depends(oauth_schemes)] = None, db: AsyncSession = Depends(get_db)):
    token_data = verify_token(token)   
    user = select(User).where(User.email == token_data.email)
    result = await db.execute(user)
    final = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="user does not exist", headers={"WWW-Authenticate": "Bearer"})
    return final

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=404, detail="Inactive user")
    return current_user

async def require_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user


async def check_login_user(user_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = select(User).filter(User.id == user_id)
    result = await db.execute(user)
    final = result.scalars().first()
    
    if not final:
        raise HTTPException(
            status_code=404,
            detail="User Not Found!"
        )
        
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="your are not login in our website!"
        )
        
    return current_user

async def check_exist_book(product_id: int, db: AsyncSession = Depends(get_db)):
    product = select(Book).filter(Book.id == product_id)
    result = await db.execute(product)
    final = result.scalars().first()
    
    if not final:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found!"
        )
        
    return final