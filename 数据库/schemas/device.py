from pydantic import BaseModel
from typing import Optional

class DeviceBase(BaseModel):
    name: str
    type: str
    room: Optional[str] = None
    status: Optional[str] = None
    owner_id: int  # 外键

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    device_id: int  # 注意使用你定义的主键名

    model_config = {
        "from_attributes": True
    }
