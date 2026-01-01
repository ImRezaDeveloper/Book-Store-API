from pydantic import BaseModel, EmailStr, Field
from .product_schemas import ProductDisplay
from typing import Annotated, Optional
import enum

class Role(str, enum.Enum):
    ADMIN = 'Admin'
    USER = 'User'


class GetUser(BaseModel):
    username: str
    email: EmailStr | None = Field(default=None)
    role: Role = Role.USER
    is_active: Annotated[bool, True] = True
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str | None
    books: list[ProductDisplay]

    model_config = {
        "from_attributes": True   # 🔥 مهمه
    }

class Token(BaseModel):
    access_token: str
    token_type: str

# Optional Field
class TokenData(BaseModel):
    email: Optional[str] = None