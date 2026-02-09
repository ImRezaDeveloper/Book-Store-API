from pydantic import BaseModel, EmailStr, Field
from .product_schemas import ProductDisplay
from typing import Annotated, Optional
import enum
# from security.auth.hashing import hash_pwd

class Role(str, enum.Enum):
    ADMIN = 'Admin'
    USER = 'User'


class UserUpdate(BaseModel):
    username: str
    email: EmailStr | None = Field(default=None)
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str | None
    role: Role
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