from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    title: str
    description: str
    price: float
    stock: int
    rating_avg: float
    rating_count: int
    
class ProductDisplay(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    stock: int
    rating_avg: float
    rating_count: int

    class Config:
        from_attributes = True