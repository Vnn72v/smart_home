
from sqlalchemy.orm import Session
from database import get_db
from models import tables
from schemas import feedback as schemas
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/feedbacks", tags=["用户反馈"])

@router.post("/", response_model=schemas.Feedback)
def create_feedback(data: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = tables.Feedback(**data.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/", response_model=list[schemas.Feedback])
def get_all_feedbacks(db: Session = Depends(get_db)):
    return db.query(tables.Feedback).all()
@router.put("/{feedback_id}", response_model=schemas.Feedback)

def update_feedback(feedback_id: int, feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = db.query(tables.Feedback).filter(tables.Feedback.feedback_id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    for key, value in feedback.dict().items():
        setattr(db_feedback, key, value)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(tables.Feedback).filter(tables.Feedback.feedback_id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    db.delete(db_feedback)
    db.commit()
    return {"message": "反馈已删除"}