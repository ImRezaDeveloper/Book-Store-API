from typing import List
from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import author_service
from app.schemas.author_schemas import Authors, AuthorDisplay

router = APIRouter(tags=['authors'], prefix='/authors')

@router.get('', status_code=200, response_model=List[AuthorDisplay])
async def get_all_authors(db: AsyncSession = Depends(get_db)):
    return await author_service.get_authors(db)

@router.post('/new', status_code=201, response_model=Authors)
async def create_author(author: Authors, db: AsyncSession = Depends(get_db)):
    return await author_service.create_author(author, db)