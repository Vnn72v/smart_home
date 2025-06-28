from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import tables
from schemas import security_event as schemas

router = APIRouter(prefix="/security_events", tags=["安防事件"])

@router.post("/", response_model=schemas.SecurityEvent)
def create_event(event: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    db_event = tables.SecurityEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=list[schemas.SecurityEvent])
def get_all_events(db: Session = Depends(get_db)):
    return db.query(tables.SecurityEvent).all()
@router.put("/{event_id}", response_model=schemas.SecurityEvent)
def update_event(event_id: int, event: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    db_event = db.query(tables.SecurityEvent).filter(tables.SecurityEvent.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="事件不存在")
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(tables.SecurityEvent).filter(tables.SecurityEvent.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="事件不存在")
    db.delete(db_event)
    db.commit()
    return {"message": "事件已删除"}
