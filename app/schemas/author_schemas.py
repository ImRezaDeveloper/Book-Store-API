from typing import Optional
from pydantic import BaseModel

class Authors(BaseModel):
    name: str
    bio: str
    
class AuthorDisplay(BaseModel):
    id: int
    name: str
    bio: str
    
    class Config:
        from_attributes = True