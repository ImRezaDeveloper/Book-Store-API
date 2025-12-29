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