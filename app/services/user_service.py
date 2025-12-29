from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select
from app.dependencies import get_db
from app.schemas.user_schemas import GetUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import User, Book
from app.security.auth.hashing import hash_pwd

app = FastAPI()

async def check_user(user_id: int, db: AsyncSession) -> User: # type: ignore
    user = select(User).where(User.id == user_id)
    result = await db.execute(user)
    final = result.scalars().first()
    
    if not final:
        raise HTTPException(status_code=404, detail="user not found")
    
    return final

async def get_users(db = get_db):
    users = select(User).options(selectinload(Book))
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
        name = user.username,
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