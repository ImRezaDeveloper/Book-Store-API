from typing import List, Optional
from pydantic import BaseModel
from .product_schemas import ProductDisplay

class Authors(BaseModel):
    name: str
    bio: str
    

class AuthorDisplay(BaseModel):
    id: int
    name: str
    bio: str | None
    books: list[ProductDisplay]

    model_config = {
        "from_attributes": True   # 🔥 مهمه
    }
    
class AuthorRegister(BaseModel):
    name: str
    bio: str
    
class AuthorUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "authorname"
            }
        }