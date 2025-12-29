
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import select
from auth.jwt_handler import verify_token
from auth.oauth2 import oauth_schemes
from app.dependencies import get_db
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user(token: Annotated[str, Depends(oauth_schemes)] = None, db: AsyncSession = Depends(get_db)):
    token_data = verify_token(token)   
    user = db.query(User).filter(User.email == token_data.email).first()
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