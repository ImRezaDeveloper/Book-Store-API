from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
# from core.config import DATABAES_URL
from app.core.config import settings

# DATABASE_URL = "postgresql+asyncpg://reza:reza.papi1384@localhost:5432/bookstoreapi"

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
