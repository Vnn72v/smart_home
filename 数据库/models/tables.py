from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# ✅ 用户表
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    house_area = Column(Float)
    email = Column(String, unique=True)
    phone = Column(String)
    age = Column(Integer)
    gender = Column(String)

    devices = relationship("Device", back_populates="owner")

# ✅ 设备表
class Device(Base):
    __tablename__ = "devices"

    device_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    status = Column(String)
    room = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="devices")

# ✅ 使用记录表
class UsageLog(Base):
    __tablename__ = "usage_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.device_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float)
    action = Column(String)

    device = relationship("Device")
    user = relationship("User")

# ✅ 安防事件表
class SecurityEvent(Base):
    __tablename__ = "security_events"

    event_id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.device_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    event_type = Column(String)
    event_time = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

    device = relationship("Device")
    user = relationship("User")

# ✅ 用户反馈表
class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    device_id = Column(Integer, ForeignKey("devices.device_id"))
    rating = Column(Integer)
    comment = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    device = relationship("Device")
