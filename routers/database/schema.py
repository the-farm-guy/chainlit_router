from pydantic import BaseModel
from typing import Optional
    
class UserUpdateModel(BaseModel):
    username: Optional[str] = None
    description: Optional[str] = None

class UserBase(BaseModel):
    username: str
    description : Optional[str] = None

class UserCreate(UserBase):
    username : str
    description : str

class UserResponse(UserBase):
    user_id: int
    username : str
    description : Optional[str] = None
    
    class Config:
        from_attributes = True  
