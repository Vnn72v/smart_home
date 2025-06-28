# schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    house_area: Optional[float]
    email: str
    phone: Optional[str]

class UserOut(BaseModel):
    user_id: int
    name: str
    house_area: float
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

    class Config:
        from_attributes = True
