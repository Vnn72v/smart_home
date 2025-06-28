import json

# ===== 示例数据体（用于 POST/PUT 请求） =====
example_bodies = {
    "user": {
        "name": "测试用户", "house_area": 80, "email": "test@example.com",
        "phone": "12345678901", "age": 28, "gender": "女"
    },
    "device": {
        "name": "智能灯", "type": "照明", "status": "在线", "room": "客厅", "owner_id": 26
    },
    "usage": {
        "device_id": 1, "user_id": 26, "duration": 15, "action": "启动"
    },
    "security": {
        "device_id": 1, "user_id": 26, "event_type": "非法入侵", "description": "测试事件"
    },
    "feedback": {
        "device_id": 1, "user_id": 26, "rating": 5, "comment": "很好"
    }
}

# ===== 构造请求函数 =====
def build_request(name, method, path, json_body=None, user_id=26):
    url_path = path.strip("/").split("/")
    if "{id}" in url_path:
        url_path = [str(user_id) if p == "{id}" else p for p in url_path]
        raw_path = path.replace("{id}", str(user_id))
    else:
        raw_path = path

    req = {
        "name": name,
        "request": {
            "method": method,
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": {
                "raw": f"http://localhost:8000{raw_path}",
                "protocol": "http",
                "host": ["localhost"],
                "port": "8000",
                "path": url_path
            }
        },
        "response": []
    }

    if method in ["POST", "PUT"] and json_body:
        req["request"]["body"] = {
            "mode": "raw",
            "raw": json.dumps(json_body, ensure_ascii=False)
        }

    return req

# ===== 所有接口构建 =====
items = []

# 用户管理接口
items += [
    build_request("创建用户", "POST", "/users/", example_bodies["user"]),
    build_request("获取所有用户", "GET", "/users/"),
    build_request("获取用户信息", "GET", "/users/{id}"),
    build_request("更新用户信息", "PUT", "/users/{id}", example_bodies["user"]),
    build_request("删除用户", "DELETE", "/users/{id}"),
    build_request("获取用户设备列表", "GET", "/users/{id}/devices"),
    build_request("获取用户使用记录", "GET", "/users/{id}/usage"),
    build_request("获取用户反馈", "GET", "/users/{id}/feedback"),
    build_request("获取用户安防事件", "GET", "/users/{id}/security_events")
]

# 设备管理接口
items += [
    build_request("创建设备", "POST", "/devices/", example_bodies["device"]),
    build_request("获取所有设备", "GET", "/devices/"),
    build_request("获取设备信息", "GET", "/devices/{id}", user_id=1),
    build_request("更新设备信息", "PUT", "/devices/{id}", example_bodies["device"], user_id=1),
    build_request("删除设备", "DELETE", "/devices/{id}", user_id=1),
]

# 使用记录接口
items += [
    build_request("创建使用记录", "POST", "/usage_logs/", example_bodies["usage"]),
    build_request("获取所有使用记录", "GET", "/usage_logs/"),
    build_request("更新使用记录", "PUT", "/usage_logs/{id}", example_bodies["usage"], user_id=1),
    build_request("删除使用记录", "DELETE", "/usage_logs/{id}", user_id=1),
]

# 安防事件接口
items += [
    build_request("创建安防事件", "POST", "/security_events/", example_bodies["security"]),
    build_request("获取所有安防事件", "GET", "/security_events/"),
    build_request("更新安防事件", "PUT", "/security_events/{id}", example_bodies["security"], user_id=1),
    build_request("删除安防事件", "DELETE", "/security_events/{id}", user_id=1),
]

# 反馈接口
items += [
    build_request("创建反馈", "POST", "/feedbacks/", example_bodies["feedback"]),
    build_request("获取所有反馈", "GET", "/feedbacks/"),
    build_request("更新反馈", "PUT", "/feedbacks/{id}", example_bodies["feedback"], user_id=1),
    build_request("删除反馈", "DELETE", "/feedbacks/{id}", user_id=1),
]

# 分析类接口
analytics = [
    ("房屋面积分布分析", "/analytics/house_area_distribution"),
    ("用户满意度分析", "/analytics/user_satisfaction"),
    ("设备使用频率分析", "/analytics/device_usage_frequency"),
    ("安防事件类型分布", "/analytics/security_event_types")
]
for name, path in analytics:
    items.append(build_request(name, "GET", path))

# ===== 构造完整 JSON 结构 =====
collection = {
    "info": {
        "_postman_id": "智能家居合集最终修复",
        "name": "智能家居接口合集（最终修复）",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": items
}

# ===== 写入文件 =====
with open("final_postman_collection.json", "w", encoding="utf-8") as f:
    json.dump(collection, f, ensure_ascii=False, indent=2)

print("✅ 已生成：final_postman_collection.json")
