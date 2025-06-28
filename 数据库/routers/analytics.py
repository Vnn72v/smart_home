from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import tables
from sqlalchemy import func, extract
from collections import defaultdict
from datetime import datetime, timedelta
from models.tables import User, Device, UsageLog
router = APIRouter(tags=["数据分析"])

@router.get("/room-count")
def count_devices_by_room(db: Session = Depends(get_db)):
    results = db.query(tables.Device.room, func.count(tables.Device.device_id)).group_by(tables.Device.room).all()
    return [{"room": room, "device_count": count} for room, count in results]

#  Q1：不同设备使用频率分析
@router.get("/device-usage-count")
def device_usage_count(db: Session = Depends(get_db)):
    result = (
        db.query(tables.Device.name, func.count(tables.UsageLog.log_id))
        .join(tables.UsageLog, tables.Device.device_id == tables.UsageLog.device_id)
        .group_by(tables.Device.name)
        .all()
    )
    return [{"device_name": name, "usage_count": count} for name, count in result]

# Q2：用户设备使用的时间分布（按小时）
@router.get("/hourly-usage")
def hourly_usage_distribution(db: Session = Depends(get_db)):
    result = (
        db.query(func.extract('hour', tables.UsageLog.timestamp), func.count(tables.UsageLog.log_id))
        .group_by(func.extract('hour', tables.UsageLog.timestamp))
        .order_by(func.extract('hour', tables.UsageLog.timestamp))
        .all()
    )
    return [{"hour": int(hour), "usage_count": count} for hour, count in result]

#  Q3：设备联动分析（同一用户同一时间段使用的设备对）
@router.get("/frequent-pairs")
def device_pair_usage(db: Session = Depends(get_db)):
    logs = db.query(tables.UsageLog).all()
    sessions = defaultdict(set)

    for log in logs:
        session_key = (log.user_id, log.timestamp.replace(minute=0, second=0, microsecond=0))  # 按小时分组
        sessions[session_key].add(log.device_id)

    pair_counts = defaultdict(int)

    for session_devices in sessions.values():
        ids = list(session_devices)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                pair = tuple(sorted((ids[i], ids[j])))
                pair_counts[pair] += 1

    # 获取设备名称
    id_name_map = {d.device_id: d.name for d in db.query(tables.Device).all()}
    result = []
    for (d1, d2), count in pair_counts.items():
        result.append({
            "device_pair": f"{id_name_map.get(d1, d1)} + {id_name_map.get(d2, d2)}",
            "count": count
        })
    return result

#  Q4：房屋面积对设备使用频率影响
@router.get("/area-usage")
def area_vs_usage(db: Session = Depends(get_db)):
    result = (
        db.query(tables.User.house_area, func.count(tables.UsageLog.log_id))
        .join(tables.UsageLog, tables.User.user_id == tables.UsageLog.user_id)
        .group_by(tables.User.house_area)
        .all()
    )
    return [{"house_area": area, "usage_count": count} for area, count in result]

# Q5：安防事件类型与时间分布
@router.get("/security-events-summary")
def security_events_summary(db: Session = Depends(get_db)):
    results = (
        db.query(
            tables.SecurityEvent.event_type,
            func.date_trunc('day', tables.SecurityEvent.event_time),
            func.count(tables.SecurityEvent.event_id)
        )
        .group_by(tables.SecurityEvent.event_type, func.date_trunc('day', tables.SecurityEvent.event_time))
        .order_by(func.date_trunc('day', tables.SecurityEvent.event_time))
        .all()
    )

    data = defaultdict(lambda: defaultdict(int))
    for event_type, date, count in results:
        data[str(date.date())][event_type] += count

    return data

# Q6：用户满意度趋势（根据评分）
@router.get("/feedback-trend")
def feedback_trend(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.date_trunc('day', tables.Feedback.timestamp),
            func.avg(tables.Feedback.rating)
        )
        .group_by(func.date_trunc('day', tables.Feedback.timestamp))
        .order_by(func.date_trunc('day', tables.Feedback.timestamp))
        .all()
    )

    return [{"date": str(date.date()), "avg_rating": float(avg)} for date, avg in results]

# Q7：单设备平均使用时长
@router.get("/house_area_distribution")
def house_area_distribution():
    return {
        "area_distribution": {
            "客厅": 3,
            "卧室": 4,
            "阳台": 2,
            "浴室": 1
        }
    }
def average_device_usage_duration(db: Session = Depends(get_db)):
    result = (
        db.query(
            tables.Device.name,
            func.avg(tables.UsageLog.duration)
        )
        .join(tables.UsageLog, tables.Device.device_id == tables.UsageLog.device_id)
        .group_by(tables.Device.name)
        .all()
    )
    return [{"device_name": name, "avg_duration": float(avg)} for name, avg in result]

@router.get("/device-average-duration")
def average_device_usage_duration(db: Session = Depends(get_db)):
    result = (
        db.query(
            tables.Device.name,
            func.avg(tables.UsageLog.duration)
        )
        .join(tables.UsageLog, tables.Device.device_id == tables.UsageLog.device_id)
        .group_by(tables.Device.name)
        .all()
    )
    return [{"device_name": name, "avg_duration": float(avg)} for name, avg in result]


# ✅ Q1-1：某个用户各设备使用频率
@router.get("/user-device-usage/{user_id}")
def user_device_usage(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(tables.Device.name, func.count(tables.UsageLog.log_id))
        .join(tables.UsageLog, tables.Device.device_id == tables.UsageLog.device_id)
        .filter(tables.UsageLog.user_id == user_id)
        .group_by(tables.Device.name)
        .all()
    )
    return [{"device_name": name, "usage_count": count} for name, count in result]

# ✅ Q1-2：某个用户设备使用时间线（甘特图数据）
@router.get("/user-device-timeline/{user_id}")
def user_device_timeline(user_id: int, db: Session = Depends(get_db)):
    logs = (
        db.query(tables.Device.name, tables.UsageLog.timestamp, tables.UsageLog.duration)
        .join(tables.Device, tables.Device.device_id == tables.UsageLog.device_id)
        .filter(tables.UsageLog.user_id == user_id)
        .order_by(tables.UsageLog.timestamp)
        .all()
    )
    return [
        {
            "device_name": name,
            "start_time": ts.isoformat(),
            "duration": duration
        } for name, ts, duration in logs
    ]

# ✅ Q2-1：某用户一天24小时使用活跃分布
@router.get("/user-usage-hour-distribution/{user_id}")
def user_hourly_distribution(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(func.extract('hour', tables.UsageLog.timestamp), func.count())
        .filter(tables.UsageLog.user_id == user_id)
        .group_by(func.extract('hour', tables.UsageLog.timestamp))
        .order_by(func.extract('hour', tables.UsageLog.timestamp))
        .all()
    )
    return [{"hour": int(hour), "usage_count": count} for hour, count in result]

# ✅ Q2-2：某用户最常用的设备TOP3
@router.get("/user-top-devices/{user_id}")
def user_top_devices(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(tables.Device.name, func.count(tables.UsageLog.log_id))
        .join(tables.UsageLog, tables.Device.device_id == tables.UsageLog.device_id)
        .filter(tables.UsageLog.user_id == user_id)
        .group_by(tables.Device.name)
        .order_by(func.count(tables.UsageLog.log_id).desc())
        .limit(3)
        .all()
    )
    total = sum(count for _, count in result)
    return [
        {"device_name": name, "percent": round(count / total * 100, 2)}
        for name, count in result
    ]

@router.get("/user-device-timeline-by-date/{user_id}")
def user_device_usage_day(user_id: int, date: str, db: Session = Depends(get_db)):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}

    start = datetime.combine(date_obj, datetime.min.time())
    end = start + timedelta(days=1)

    logs = (
        db.query(tables.Device.name, tables.UsageLog.timestamp, tables.UsageLog.duration)
        .join(tables.Device, tables.Device.device_id == tables.UsageLog.device_id)
        .filter(tables.UsageLog.user_id == user_id)
        .filter(tables.UsageLog.timestamp >= start, tables.UsageLog.timestamp < end)
        .all()
    )

    return [
        {
            "device_name": name,
            "start_time": ts.isoformat(),
            "duration": duration
        } for name, ts, duration in logs
    ]

# ✅ 用户：某设备每日使用时长（分钟）
@router.get("/user-device-daily-duration/{user_id}")
def user_device_daily_duration(user_id: int, device_name: str = Query(...), db: Session = Depends(get_db)):
    logs = (
        db.query(
            func.date_trunc('day', tables.UsageLog.timestamp).label("day"),
            func.sum(tables.UsageLog.duration)
        )
        .join(tables.Device, tables.Device.device_id == tables.UsageLog.device_id)
        .filter(tables.UsageLog.user_id == user_id, tables.Device.name == device_name)
        .group_by("day")
        .order_by("day")
        .all()
    )

    return [{"date": str(day.date()), "total_minutes": float(minutes)} for day, minutes in logs]

# ✅ 用户：每小时用电分布（用于G1用户版）
@router.get("/user-hourly-usage/{user_id}")
def user_hourly_usage(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            extract('hour', tables.UsageLog.timestamp),
            func.count()
        )
        .filter(tables.UsageLog.user_id == user_id)
        .group_by(extract('hour', tables.UsageLog.timestamp))
        .order_by(extract('hour', tables.UsageLog.timestamp))
        .all()
    )
    return [{"hour": int(hour), "usage_count": count} for hour, count in result]

# ✅ 用户版反馈趋势
@router.get("/user-feedback-trend/{user_id}")
def user_feedback_trend(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            func.date_trunc('day', tables.Feedback.timestamp),
            func.avg(tables.Feedback.rating)
        )
        .filter(tables.Feedback.user_id == user_id)
        .group_by(func.date_trunc('day', tables.Feedback.timestamp))
        .order_by(func.date_trunc('day', tables.Feedback.timestamp))
        .all()
    )
    return [{"date": str(date.date()), "avg_rating": float(score)} for date, score in result]

# ✅ 用户版 area usage（可选）
@router.get("/user-area-usage/{user_id}")
def user_area_usage(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            tables.User.house_area,
            func.count(tables.UsageLog.log_id)
        )
        .join(tables.UsageLog, tables.User.user_id == tables.UsageLog.user_id)
        .filter(tables.User.user_id == user_id)
        .group_by(tables.User.house_area)
        .all()
    )
    return [{"house_area": area, "usage_count": count} for area, count in result]
@router.get("/user-frequent-pairs/{user_id}")
def user_frequent_pairs(user_id: int, db: Session = Depends(get_db)):
    from collections import Counter
    from itertools import combinations

    logs = (
        db.query(tables.UsageLog.device_id, tables.UsageLog.timestamp)
        .filter(tables.UsageLog.user_id == user_id)
        .all()
    )
    if not logs:
        return []

    # 构造 同一小时内使用的设备组合
    device_by_hour = {}
    for device_id, ts in logs:
        hour_key = ts.replace(minute=0, second=0, microsecond=0)
        device_by_hour.setdefault(hour_key, []).append(device_id)

    pair_counter = Counter()
    for device_list in device_by_hour.values():
        if len(device_list) >= 2:
            for pair in combinations(sorted(set(device_list)), 2):
                pair_counter[pair] += 1

    # 取设备名称
    device_map = {d.device_id: d.name for d in db.query(tables.Device).all()}
    result = [
        {"device_pair": f"{device_map.get(a, a)} + {device_map.get(b, b)}", "count": c}
        for (a, b), c in pair_counter.items()
    ]
    result.sort(key=lambda x: x["count"], reverse=True)
    return result
@router.get("/user-area-usage/{user_id}")
def user_area_usage(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(tables.User.house_area, func.count(tables.UsageLog.log_id))
        .join(tables.UsageLog, tables.User.user_id == tables.UsageLog.user_id)
        .filter(tables.User.user_id == user_id)
        .group_by(tables.User.house_area)
        .all()
    )
    return [{"house_area": float(a), "usage_count": int(c)} for a, c in result]
@router.get("/user-device-average-duration/{user_id}")
def user_device_avg_duration(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(tables.Device.name, func.avg(tables.UsageLog.duration))
        .join(tables.Device, tables.Device.device_id == tables.UsageLog.device_id)
        .filter(tables.UsageLog.user_id == user_id)
        .group_by(tables.Device.name)
        .all()
    )
    return [{"device_name": name, "avg_duration": round(avg, 2)} for name, avg in result]
@router.get("/user-security-events-summary/{user_id}")
def user_security_events(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            func.date_trunc('day', tables.SecurityEvent.event_time).label("day"),
            tables.SecurityEvent.event_type,
            func.count()
        )
        .filter(tables.SecurityEvent.user_id == user_id)
        .group_by("day", tables.SecurityEvent.event_type)
        .all()
    )

    summary = {}
    for day, event_type, count in result:
        date_str = str(day.date())
        if date_str not in summary:
            summary[date_str] = {}
        summary[date_str][event_type] = count

    return summary
@router.get("/area-device-usage")
@router.get("/area-device-usage")
def area_device_usage(db: Session = Depends(get_db)):
    result = (
        db.query(
            User.user_id,
            User.house_area,
            Device.name.label("device_name"),
            func.avg(UsageLog.duration).label("avg_duration"),
            func.count(UsageLog.log_id).label("avg_count")
        )
        .join(Device, Device.owner_id == User.user_id)
        .join(UsageLog, (UsageLog.user_id == User.user_id) & (UsageLog.device_id == Device.device_id))
        .group_by(User.user_id, User.house_area, Device.name)
        .all()
    )

    return [
        {
            "house_area": row.house_area,
            "device_name": row.device_name,
            "avg_duration": float(row.avg_duration),
            "avg_count": float(row.avg_count)
        }
        for row in result
    ]
