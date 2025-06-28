# simulate_realistic_data.py
from datetime import datetime, timedelta
import random
from database import SessionLocal
from models.tables import User, Device, UsageLog, Feedback, SecurityEvent
from sqlalchemy.exc import IntegrityError

db = SessionLocal()

# ✅ 删除顺序必须考虑外键依赖
db.query(Feedback).delete()
db.query(UsageLog).delete()
db.query(SecurityEvent).delete()
db.query(Device).delete()
db.query(User).delete()
db.commit()

# ✅ 模拟用户数据
names = ["张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十", "钱十一", "冯十二"]
user_profiles = []
for i, name in enumerate(names):
    user_profiles.append({
        "name": name,
        "area": random.choice([45, 60, 75, 90, 110, 130]),
        "gender": random.choice(["男", "女"]),
        "age": random.randint(20, 55),
        "phone": f"18800000{i:04d}"
    })

device_catalog = {
    "共通": ["冰箱", "空调", "电视", "抽油烟机", "微波炉"],
    "小户型": ["台灯", "洗衣机"],
    "中户型": ["台灯", "洗衣机", "风扇", "电饭煲"],
    "大户型": ["洗衣机", "风扇", "空气净化器", "烘干机", "窗帘", "加湿器"]
}

device_usage_patterns = {
    "冰箱": {"base_hour": 7, "duration": (30, 60), "freq": 0.9},
    "空调": {"base_hour": 15, "duration": (180, 300), "freq": 0.8},
    "电视": {"base_hour": 20, "duration": (60, 180), "freq": 0.7},
    "洗衣机": {"base_hour": 21, "duration": (40, 60), "freq": 0.5},
    "烘干机": {"base_hour": 22, "duration": (30, 45), "freq": 0.4},
    "微波炉": {"base_hour": 7.5, "duration": (10, 20), "freq": 0.6},
    "抽油烟机": {"base_hour": 18, "duration": (20, 40), "freq": 0.6},
    "台灯": {"base_hour": 23, "duration": (60, 120), "freq": 0.5},
    "空气净化器": {"base_hour": 10, "duration": (300, 600), "freq": 0.4},
    "风扇": {"base_hour": 16, "duration": (60, 120), "freq": 0.6},
    "窗帘": {"base_hour": 6, "duration": (2, 5), "freq": 0.2},
    "加湿器": {"base_hour": 2, "duration": (90, 180), "freq": 0.3},
    "电饭煲": {"base_hour": 12, "duration": (45, 60), "freq": 0.4},
}

start_date = datetime(2025, 6, 1)
days = 30
all_devices = []

# ✅ 插入用户和设备
for user in user_profiles:
    u = User(
        name=user["name"],
        house_area=user["area"],
        email=f"{user['name']}@test.com",
        phone=user["phone"],
        age=user["age"],
        gender=user["gender"]
    )
    db.add(u)
    db.flush()
    uid = u.user_id

    # 分配设备
    if user["area"] < 70:
        devices = device_catalog["共通"] + device_catalog["小户型"]
    elif user["area"] < 110:
        devices = device_catalog["共通"] + device_catalog["中户型"]
    else:
        devices = device_catalog["共通"] + device_catalog["大户型"]

    device_objs = {}
    for dev in devices:
        d = Device(name=dev, owner_id=uid, room="默认", status="在线", type="电器")
        db.add(d)
        db.flush()
        device_objs[dev] = d
        all_devices.append((uid, d.device_id, dev))

    # 插入使用记录
    for dev_name in devices:
        if dev_name not in device_usage_patterns:
            continue
        pattern = device_usage_patterns[dev_name]
        for d in range(days):
            if random.random() > pattern["freq"]:
                continue
            ts = start_date + timedelta(days=d, hours=pattern["base_hour"] + random.uniform(-1.5, 1.5))
            dur = round(random.uniform(*pattern["duration"]), 2)
            log = UsageLog(
                user_id=uid,
                device_id=device_objs[dev_name].device_id,
                timestamp=ts,
                duration=dur,
                action="开启"
            )
            db.add(log)

    # 插入反馈（每人选几个设备评分）
    for dev in random.sample(list(device_objs.values()), k=3):
        feedback = Feedback(
            user_id=uid,
            device_id=dev.device_id,
            rating=random.randint(2, 5),
            comment=random.choice([
                "设备很方便", "使用流畅", "偶尔卡顿", "体验一般", "挺好的"
            ]),
            timestamp=start_date + timedelta(days=random.randint(1, days))
        )
        db.add(feedback)

    # 插入安防事件（每人选1~2台设备）
    for dev in random.sample(list(device_objs.values()), k=2):
        event = SecurityEvent(
            user_id=uid,
            device_id=dev.device_id,
            event_type=random.choice(["异常断电", "非法操作", "远程开机"]),
            description=random.choice(["门锁异常开启", "电压波动", "网络干扰"]),
            event_time=start_date + timedelta(days=random.randint(1, days))
        )
        db.add(event)

try:
    db.commit()
except IntegrityError as e:
    db.rollback()
    print("❌ 插入失败，请检查字段约束")
    print(e)
else:
    print("✅ 模拟完整数据生成完毕")
finally:
    db.close()
