from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import tables
from schemas import device as schemas
from typing import List

router = APIRouter(prefix="/devices", tags=["设备"])

@router.post("/", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = tables.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/", response_model=list[schemas.Device])
def read_devices(db: Session = Depends(get_db)):
    return db.query(tables.Device).all()

@router.get("/{device_id}", response_model=schemas.Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(tables.Device).filter(tables.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.get("/users/{user_id}/devices", response_model=List[schemas.Device])
def get_devices_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(tables.Device).filter(tables.Device.owner_id == user_id).all()
@router.put("/{device_id}", response_model=schemas.Device)
def update_device(device_id: int, device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = db.query(tables.Device).filter(tables.Device.device_id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="设备不存在")
    for key, value in device.dict().items():
        setattr(db_device, key, value)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(tables.Device).filter(tables.Device.device_id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="设备不存在")
    db.delete(db_device)
    db.commit()
    return {"message": "设备已删除"}
