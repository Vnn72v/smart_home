from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import tables
from schemas import usage_log as schemas

router = APIRouter(prefix="/usage_logs", tags=["使用记录"])

@router.post("/", response_model=schemas.UsageLog)
def create_usage_log(log: schemas.UsageLogCreate, db: Session = Depends(get_db)):
    db_log = tables.UsageLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/", response_model=list[schemas.UsageLog])
def get_all_logs(db: Session = Depends(get_db)):
    return db.query(tables.UsageLog).all()
@router.put("/{log_id}", response_model=schemas.UsageLog)
def update_usage_log(log_id: int, log: schemas.UsageLogCreate, db: Session = Depends(get_db)):
    db_log = db.query(tables.UsageLog).filter(tables.UsageLog.log_id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    for key, value in log.dict().items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/{log_id}")
def delete_usage_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(tables.UsageLog).filter(tables.UsageLog.log_id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    db.delete(db_log)
    db.commit()
    return {"message": "使用记录已删除"}
