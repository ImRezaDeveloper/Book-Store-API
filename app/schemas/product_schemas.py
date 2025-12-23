from pydantic import BaseModel


class Product(BaseModel):
    title: str
    description: str
    price: float
    stock: int
    rating_avg: float
    rating_count: int
    
class ProductDisplay(BaseModel):
    title: str
    description: str
    price: float
    stock: int
    rating_avg: float
    rating_count: int
    
    class Config:
        orm_mode=True