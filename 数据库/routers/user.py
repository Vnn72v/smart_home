# routers/user.py
from schemas.user import UserCreate, UserOut
from schemas.user import UserOut  # 你已有这个
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from models.tables import User
from sqlalchemy.orm import Session
from database import get_db
from models import tables
from schemas import device as schemas
from typing import List
from schemas.usage_log import UsageLog
from schemas.feedback import Feedback
from schemas.security_event import SecurityEvent



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# routers/user.py
@router.get("/users/{user_id}/devices", response_model=List[schemas.Device])
def get_devices_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(tables.Device).filter(tables.Device.owner_id == user_id).all()

@router.get("/users/{user_id}/usage", response_model=List[UsageLog])
def get_user_usage(user_id: int, db: Session = Depends(get_db)):
    return db.query(tables.UsageLog).filter(tables.UsageLog.user_id == user_id).all()
@router.get("/users/{user_id}/feedback", response_model=List[Feedback])
def get_user_feedback(user_id: int, db: Session = Depends(get_db)):
    return db.query(tables.Feedback).filter(tables.Feedback.user_id == user_id).all()
@router.get("/users/{user_id}/security_events", response_model=List[SecurityEvent])
def get_user_security_events(user_id: int, db: Session = Depends(get_db)):
    return db.query(tables.SecurityEvent).filter(tables.SecurityEvent.user_id == user_id).all()

from schemas.user import UserCreate

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(db_user)
    db.commit()
    return {"message": "用户已删除"}
