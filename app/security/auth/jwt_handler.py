from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from app.core.config import settings
from app.schemas.user_schemas import TokenData
from jose import jwt

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not verify Creditials", headers={"WWW-Authenticate": "Bearer"})
        return TokenData(email=email)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not verify Creditials", headers={"WWW-Authenticate": "Bearer"})