from app.db.database import SessionlLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionlLocal()
    try:
        yield db
    finally:
        db.close()