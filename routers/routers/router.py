from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.model import User
from database.database import get_db
from database.schema import UserResponse, UserBase, UserCreate

router = APIRouter(
    prefix="/api/v1",
    tags=["users"]
)

@router.get("/users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/users/{username}", response_model = UserResponse)
async def get_user(username : str, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise HTTPException(status_code = 404, details = 'user not found')
    return user
    
@router.post('/user', response_model = UserResponse)
async def create_user(data : UserCreate, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    
    if user:
        raise HTTPException(status_code = 400, detail = 'user already exists')
    
    else:
        new_user = User(username = data.username, description = data.description)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user