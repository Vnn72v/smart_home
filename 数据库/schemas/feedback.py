from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class FeedbackBase(BaseModel):
    user_id: int
    device_id: int
    rating: int  # 1-5
    timestamp: datetime
    description: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    feedback_id: int

    model_config = {
        "from_attributes": True
    }
