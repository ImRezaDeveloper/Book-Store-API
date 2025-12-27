from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from app.dependencies import get_db
from app.models.author import Author
from app.schemas.author_schemas import Authors
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

async def get_authors(db: AsyncSession = Depends(get_db)):
    authors = select(Author)
    result = await db.execute(authors)
    final = result.scalars().all()
    if not final:
        raise HTTPException(
            status_code=404,
            detail="DB is empty!"
        )
    return final

async def create_author(author: Authors, db: AsyncSession) -> Author:
    new_author = Author(
        name = author.name,
        bio = author.bio
    )
    
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author