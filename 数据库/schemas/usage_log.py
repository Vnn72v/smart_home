from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsageLogBase(BaseModel):
    device_id: int
    user_id: int
    timestamp: datetime
    duration: float
    action: Optional[str] = None

class UsageLogCreate(UsageLogBase):
    pass

class UsageLog(UsageLogBase):
    log_id: int

    model_config = {
        "from_attributes": True
    }
