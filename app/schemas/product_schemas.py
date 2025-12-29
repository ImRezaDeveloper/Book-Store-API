from typing import List, Optional
from pydantic import BaseModel
from typing import Annotated

from app.models.author import Author


class Product(BaseModel):
    title: str
    description: str
    price: float
    stock: int
    rating_avg: float
    rating_count: int
    author_id: int
    
class ProductDisplay(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    stock: int
    rating_avg: float
    rating_count: int

    model_config = {
        "from_attributes": True   # 🔥 مهمه
    }
