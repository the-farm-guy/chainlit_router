from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.model import User
from database.database import get_db
from database.schema import UserResponse, UserCreate, UserUpdateModel

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

@router.patch("/user/{username}", response_model=UserResponse)
async def update_user(
    username: str,
    user_update: UserUpdateModel,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username and user_update.username != username:
        existing = db.query(User).filter(User.username == user_update.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)

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
    
@router.delete('/user', response_model = UserResponse)
async def delete_user(username : str, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise HTTPException(status_code = 404, detail = 'user not found')
    
    else:
        db.delete(user)
        db.commit()
        return user
