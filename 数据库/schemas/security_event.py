from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SecurityEventBase(BaseModel):
    device_id: int
    user_id: int
    event_type: str
    event_time: datetime
    description: Optional[str] = None

class SecurityEventCreate(SecurityEventBase):
    pass

class SecurityEvent(SecurityEventBase):
    event_id: int

    model_config = {
        "from_attributes": True
    }
