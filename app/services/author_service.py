from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select
from app.dependencies import get_db
from app.models.author import Author
from app.schemas.author_schemas import Authors
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

app = FastAPI()

async def check_author(author_id: int, db: AsyncSession) -> Author: # type: ignore
    author = select(Author).where(Author.id == author_id)
    result = await db.execute(author)
    final = result.scalars().first()
    
    if not final:
        raise HTTPException(status_code=404, detail="the author not found")
    
    return final

async def get_authors(db = get_db):
    authors = select(Author).options(selectinload(Author.books))
    result = await db.execute(authors)
    final = result.scalars().all()
    if not final:
        raise HTTPException(
            status_code=404,
            detail="DB is empty!"
        )
    return final

async def get_author_by_id(author_id: int, db = Depends(get_db)):
    author = select(Author).where(Author.id == author_id).options(selectinload(Author.books))
    result = await db.execute(author)
    final = result.scalars().first()
    
    if not final:
        raise HTTPException(status_code=404, detail="the author not found with this id!")

    return final

async def create_author(author: Authors, db = Depends(get_db)) -> Author:
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