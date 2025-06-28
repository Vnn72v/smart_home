# generate_test_user_data.py
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from database import SessionLocal
from models.tables import User, Device, UsageLog, Feedback, SecurityEvent

def generate_test_user():
    db: Session = SessionLocal()

    # 1. 创建用户
    test_user = User(
        name="测试员",
        age=35,
        gender="男",
        house_area=120,
        email=f"test{random.randint(1000,9999)}@example.com",
        phone="13800000000"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print(f"✅ 创建用户：{test_user.name}（user_id={test_user.user_id}）")

    # 2. 创建设备
    device_names = ["智能门锁", "监控摄像头", "空调", "智能灯"]
    devices = []
    for name in device_names:
        d = Device(name=name, type="智能设备", status="在线", room="客厅", owner_id=test_user.user_id)
        db.add(d)
        devices.append(d)
    db.commit()
    db.refresh(devices[0])  # 确保设备id被填充

    # 3. 生成使用日志（近30天，每台设备每日1-2条）
    start_date = datetime.now() - timedelta(days=30)
    for day_offset in range(30):
        base_time = start_date + timedelta(days=day_offset)
        for device in devices:
            for _ in range(random.randint(1, 2)):
                log = UsageLog(
                    device_id=device.device_id,
                    user_id=test_user.user_id,
                    timestamp=base_time + timedelta(minutes=random.randint(0, 1430)),
                    duration=random.uniform(10, 60),
                    action=random.choice(["开机", "关机", "调节"])
                )
                db.add(log)

    # 4. 添加安防事件（20条）
    event_types = ["入侵", "报警", "烟雾", "异常移动"]
    for _ in range(20):
        event = SecurityEvent(
            user_id=test_user.user_id,
            device_id=random.choice(devices).device_id,
            event_type=random.choice(event_types),
            event_time=start_date + timedelta(days=random.randint(0, 29), minutes=random.randint(0, 1440)),
            description="测试自动生成的安防事件"
        )
        db.add(event)

    # 5. 添加满意度反馈（30天，每天1条）
    for day_offset in range(30):
        fb = Feedback(
            user_id=test_user.user_id,
            device_id=random.choice(devices).device_id,
            rating=random.randint(3, 5),
            comment=random.choice(["不错", "满意", "系统稳定", "还可以"]),
            timestamp=start_date + timedelta(days=day_offset, minutes=random.randint(0, 1200))
        )
        db.add(fb)

    db.commit()
    db.close()
    print("✅ 测试用户数据生成完毕")

if __name__ == "__main__":
    generate_test_user()
