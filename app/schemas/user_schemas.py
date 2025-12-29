from pydantic import BaseModel, EmailStr, Field
from .product_schemas import ProductDisplay


class GetUser(BaseModel):
    username: str
    email: EmailStr | None = Field(default=None)
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str | None
    books: list[ProductDisplay]

    model_config = {
        "from_attributes": True   # 🔥 مهمه
    }