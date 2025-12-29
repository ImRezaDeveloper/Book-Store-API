from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select
from app.dependencies import get_db
from app.models.author import Author
from app.schemas.author_schemas import Authors
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import User, Book

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

async def create_user(user: Authors, db = Depends(get_db)) -> Author:
    new_author = Author(
        name = author.name,
        bio = author.bio
    )
    
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author

async def update_author(author_id: int, request: Authors, db: AsyncSession = Depends(get_db)):
    author = await check_author(author_id=author_id, db=db)
    
    updated_author = request.model_dump(exclude_unset=True)
    
    for key, value in updated_author.items():
        setattr(author, key, value)
        
    await db.commit()
    await db.refresh(author)
    
    return author

async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    author = await check_author(author_id=author_id, db=db)
        
    await db.delete(author)
    await db.commit()
        
    return Response('user was deleted successfully')