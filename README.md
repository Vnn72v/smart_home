# smart_home
期末项目：选题二 设计一个智能家居系统

# 🏠 智能家居数据库系统

雷雯娟 42233072
杨媛媛 42233073

> 基于 FastAPI + SQLAlchemy + PostgreSQL 实现的智能家居数据平台，支持设备、用户、使用日志、安防事件等多类资源的完整增删改查，并提供可视化分析、模拟数据生成与接口测试等工具。


---

## 📚 目录

1. [安装与运行说明](#1-安装与运行说明)
2. [项目结构说明](#2-项目结构说明智能家居数据库系统)
3. [接口介绍总表（基于 router 文件夹）](#3-接口介绍总表基于-router-文件夹)
4. [测试数据集设计说明](#4-测试数据集设计说明)
5. [可视化模块说明](#5-可视化模块说明)
6. [Postman 接口测试集](#6-postman接口测试集)

---

## 1. 安装与运行说明

本项目基于 **Python + FastAPI + SQLAlchemy + PostgreSQL** 开发，以下是完整的部署与运行流程。

### (1) 环境准备

```
# （可选）创建虚拟环境
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
```
(2) 数据库配置
本项目默认使用 PostgreSQL 作为数据库引擎。

确保 PostgreSQL 已正确安装 并启动服务。

创建数据库
```
smart_home
CREATE DATABASE smart_home;
配置 .env 文件中的数据库连接字符串

DATABASE_URL=postgresql://username:password@localhost:5432/smart_home
```
(3) 初始化测试数据（任选其一）
执行以下任一脚本，用于创建表结构并填充模拟数据：
```
# 创建单个测试用户（轻量测试）
python scripts/generate_test_user_data.py

# 创建多个用户及完整使用行为（适合可视化分析）
python scripts/simulate_realistic_data.py
首次运行将自动建表并插入数据，无需手动创建表。
```
(4) 启动服务
```
uvicorn main:app --reload
服务默认运行在：

http://127.0.0.1:8000
```
(5) 可视化生成（可选）
运行以下脚本，即可根据 API 返回的数据生成图表：
```
# 管理员视角：生成 G1–G9 图表
python visualize_admin.py

# 用户视角：需输入用户ID、日期与设备名，生成 U1–U4 + 用户版 G 图
python visualize_user.py
```
图表将自动保存在当前目录，命名如 G1_device_freq.png、U2_user2_2025-06-27_gantt.png 等。

# 2. 项目结构说明智能家居数据库系统
```bash
项目根目录/
├── __pycache__/                  # Python 缓存目录，无需关注
├── venv/                         # 虚拟环境目录（存放第三方包）
├── .env                          # 环境变量配置文件（如数据库连接）
├── requirements.txt              # Python 项目依赖包列表
├── database.py                   # 数据库连接配置与 Session 管理
├── main.py                       # FastAPI 主入口，挂载各路由模块
│
├── models/                       # ORM 模型定义
│   └── tables.py                 # 定义 User、Device、Feedback 等数据库模型
│
├── schemas/                      # 数据传输结构定义（Pydantic）
│   ├── device.py                 # 设备 Device 的请求/响应模型
│   ├── feedback.py               # 用户反馈 Feedback 的请求/响应模型
│   ├── security_event.py         # 安防事件 SecurityEvent 的请求/响应模型
│   ├── usage_log.py              # 使用记录 UsageLog 的请求/响应模型
│   └── user.py                   # 用户 User 的请求/响应模型
│
├── routers/                      # 路由与接口定义模块
│   ├── analytics.py              # 分析类接口（G1-G9，可视化用数据查询）
│   ├── device.py                 # 设备管理接口（增删查改）
│   ├── feedback.py               # 用户反馈接口（增删查改）
│   ├── security_event.py         # 安防事件接口（增删查改）
│   ├── usage_log.py              # 使用记录接口（增删查改）
│   └── user.py                   # 用户管理 + 多类型查询接口（含多表联查）
│
├── scripts/                      # 数据生成与测试脚本
│   ├── generate_test_user_data.py    # 用于创建单个测试用户及完整行为链
│   └── simulate_realistic_data.py    # 模拟多个用户、不同户型与行为数据
│
├── visualize_admin.py            # 管理员视角可视化脚本（生成 G1–G9 图表）
├── visualize_user.py             # 用户视角可视化脚本（生成 U1–U4 + 用户版 G 图）
│
├── G1_device_freq.png            # 以下为可视化自动保存生成的图片文件
├── G1_hourly_usage.png
├── G2_frequent_pairs.png
├── G3_area_vs_usage.png
├── G4_avg_duration.png
├── G5_feedback_trend.png
├── G6_security_events.png
├── G7_area_usage_bar.png
├── G8_area_device_duration.png
└── G9_area_device_frequency.png
```

## 3. 接口介绍总表（基于 router 文件夹）
| 模块文件名          | 接口路径                                                     | 接口功能说明                             |
| ------------------- | ------------------------------------------------------------ | ---------------------------------------- |
| `user.py`           | `POST /users/`                                               | 创建用户                                 |
| `user.py`           | `GET /users`                                                 | 获取所有用户列表                         |
| `user.py`           | `GET /users/{user_id}`                                       | 获取指定用户的详细信息                   |
| `user.py`           | `PUT /users/{user_id}`                                       | 修改用户信息                             |
| `user.py`           | `DELETE /users/{user_id}`                                    | 删除用户                                 |
| `user.py`           | `GET /users/{user_id}/devices`                               | 获取指定用户的所有设备                   |
| `user.py`           | `GET /users/{user_id}/usage`                                 | 获取指定用户的设备使用记录               |
| `user.py`           | `GET /users/{user_id}/feedback`                              | 获取指定用户的反馈列表                   |
| `user.py`           | `GET /users/{user_id}/security_events`                       | 获取指定用户的安防事件                   |
| `device.py`         | `POST /devices/`                                             | 创建设备                                 |
| `device.py`         | `GET /devices/`                                              | 获取所有设备                             |
| `device.py`         | `GET /devices/{device_id}`                                   | 获取指定设备信息                         |
| `device.py`         | `PUT /devices/{device_id}`                                   | 更新设备信息                             |
| `device.py`         | `DELETE /devices/{device_id}`                                | 删除设备                                 |
| `feedback.py`       | `POST /feedbacks/`                                           | 创建用户反馈                             |
| `feedback.py`       | `GET /feedbacks/`                                            | 获取所有用户反馈                         |
| `feedback.py`       | `PUT /feedbacks/{feedback_id}`                               | 更新指定反馈                             |
| `feedback.py`       | `DELETE /feedbacks/{feedback_id}`                            | 删除指定反馈                             |
| `security_event.py` | `POST /security_events/`                                     | 创建安防事件                             |
| `security_event.py` | `GET /security_events/`                                      | 获取所有安防事件                         |
| `security_event.py` | `PUT /security_events/{event_id}`                            | 更新指定安防事件                         |
| `security_event.py` | `DELETE /security_events/{event_id}`                         | 删除指定安防事件                         |
| `usage_log.py`      | `POST /usage_logs/`                                          | 创建使用记录                             |
| `usage_log.py`      | `GET /usage_logs/`                                           | 获取所有使用记录                         |
| `usage_log.py`      | `PUT /usage_logs/{log_id}`                                   | 更新指定使用记录                         |
| `usage_log.py`      | `DELETE /usage_logs/{log_id}`                                | 删除指定使用记录                         |
| `analytics.py`      | `GET /analytics/device-usage-count`                          | 获取所有设备的使用频率                   |
| `analytics.py`      | `GET /analytics/hourly-usage`                                | 获取每小时用电趋势                       |
| `analytics.py`      | `GET /analytics/frequent-pairs`                              | 获取最常被配对使用的设备组合             |
| `analytics.py`      | `GET /analytics/area-usage`                                  | 获取不同面积房屋的用电统计               |
| `analytics.py`      | `GET /analytics/device-average-duration`                     | 获取各设备的平均使用时长                 |
| `analytics.py`      | `GET /analytics/feedback-trend`                              | 获取系统整体的满意度趋势                 |
| `analytics.py`      | `GET /analytics/security-events-summary`                     | 获取所有安防事件按天统计                 |
| `analytics.py`      | `GET /analytics/area-device-usage`                           | 获取设备在各类面积房屋中的日均时长与频次 |
| `analytics.py`      | `GET /analytics/user-hourly-usage/{id}`                      | 获取某用户的每小时使用趋势               |
| `analytics.py`      | `GET /analytics/user-frequent-pairs/{id}`                    | 获取某用户常见设备共用组合               |
| `analytics.py`      | `GET /analytics/user-device-average-duration/{id}`           | 获取某用户各设备平均使用时长             |
| `analytics.py`      | `GET /analytics/user-feedback-trend/{id}`                    | 获取某用户的满意度趋势                   |
| `analytics.py`      | `GET /analytics/user-security-events-summary/{id}`           | 获取某用户的安防事件类型分布图           |
| `analytics.py`      | `GET /analytics/user-device-usage/{id}`                      | 获取用户各设备的使用频率                 |
| `analytics.py`      | `GET /analytics/user-device-timeline-by-date/{id}?date=YYYY-MM-DD` | 获取某日的设备使用甘特图                 |
| `analytics.py`      | `GET /analytics/user-device-daily-duration/{id}?device_name=XXX` | 获取指定设备每日使用时长                 |
| `analytics.py`      | `GET /analytics/user-top-devices/{id}`                       | 获取用户 Top3 使用设备占比（用于饼图）   |

## 4. 测试数据集设计说明
系统配套设计了两类数据生成脚本，用于测试不同层次的业务场景：

------

### (1)  `generate_test_user_data.py`：单用户完整行为模拟

> 目标：用于调试单用户视图、前端快速测试。

- **生成内容**：26
  - 单一测试用户（带 4 台智能设备）
  - 每台设备生成近 30 天的使用记录（1–2 次/天）
  - 生成 20 条安防事件（模拟随机类型）
  - 每天生成 1 条满意度反馈
- **特点**：数据精简，覆盖面广，适合 API 回调测试。

------

###  (2) `simulate_realistic_data.py`：真实多用户行为模拟

> 目标：用于全局图表分析、高维特征模拟。

- **用户规模**：10 位中文名用户，住房面积与年龄性别各异
- **设备分配**：按户型大小分配设备组合（小/中/大户型差异化）
- **使用日志生成**：
  - 按设备“使用模式”生成（如空调高频在 15 点附近开启）
  - 控制使用频率与时长，模拟家庭电器行为
- **反馈与事件**：每人生成 3 条评分，2 条安防事件
- **特点**：数据密集、行为规律化，适合建模与聚合分析

## 5. 可视化模块说明
系统设计了两个主要视角的可视化模块：

------

### 👨‍💼 **管理员视角 `visualize_admin.py`**

> 不依赖用户 ID，聚焦全局趋势分析，图表编号 G1–G9。

| 图表编号 | 图表名称                     | 接口数据                                | 功能说明                               |
| -------- | ---------------------------- | --------------------------------------- | -------------------------------------- |
| G1       | 设备使用频率 + 每小时趋势    | `/device-usage-count` + `/hourly-usage` | 展示所有设备总体使用频次和用电时段高峰 |
| G2       | 设备配对共用频率             | `/frequent-pairs`                       | 统计最常同时使用的设备组合             |
| G3       | 房屋面积 vs 用电次数         | `/area-usage`                           | 探索住房面积对总使用量的影响           |
| G4       | 各设备平均使用时长           | `/device-average-duration`              | 各类设备的平均使用分钟数               |
| G5       | 每日平均满意度趋势           | `/feedback-trend`                       | 用户评分的时间变化趋势                 |
| G6       | 每日安防事件堆叠图           | `/security-events-summary`              | 按日期分类展示各类安防事件数量         |
| G7       | 不同面积用户的用电统计       | `/area-usage`                           | 对不同面积段聚合后的使用频率           |
| G8       | 面积 vs 设备（日均使用时长） | `/area-device-usage`                    | 气泡图展示设备在不同面积住宅的使用时长 |
| G9       | 面积 vs 设备（日均使用频次） | `/area-device-usage`                    | 频次气泡图，体现使用活跃度             |

------

### 👤 **用户视角 `visualize_user.py`**

> 结合用户 ID，展示个性化用电行为、安防反馈与设备习惯，图表编号 G1–G5、U1–U4。

#### 📈 G 类：

| 图表编号 | 图表名称           | 接口                                 | 功能说明                   |
| -------- | ------------------ | ------------------------------------ | -------------------------- |
| G1       | 每小时使用趋势     | `/user-hourly-usage/{id}`            | 分析用户使用行为的时间习惯 |
| G2       | 设备配对共用频率   | `/user-frequent-pairs/{id}`          | 个体常见设备组合统计       |
| G3       | 各设备平均使用时长 | `/user-device-average-duration/{id}` | 个人各设备平均使用量       |
| G4       | 满意度趋势         | `/user-feedback-trend/{id}`          | 用户打分趋势图             |
| G5       | 安防事件分布图     | `/user-security-events-summary/{id}` | 彩色散点图按类型标注       |

#### 🧠 U 类：

| 图表编号 | 图表名称               | 接口                                            | 功能说明               |
| -------- | ---------------------- | ----------------------------------------------- | ---------------------- |
| U1       | 设备使用频率           | `/user-device-usage/{id}`                       | 各设备的使用次数柱状图 |
| U2       | 日度设备使用甘特图     | `/user-device-timeline-by-date/{id}?date=xxx`   | 时间轴还原使用场景     |
| U3       | 某设备每日使用时长     | `/user-device-daily-duration/{id}?device_name=` | 日历式行为趋势         |
| U4       | 用户设备使用 Top3 饼图 | `/user-top-devices/{id}`                        | 最常用设备占比情况     |

## 6. postman接口测试集
已经制作好指令的json文件，具体操作包括：

Fetched contentFetched content
### ✅ 包含内容：

- 用户接口（创建、获取、更新、删除）
- 设备接口（创建、获取、更新、删除）
- 使用记录接口（创建、获取、更新、删除）
- 安防事件接口（创建、获取、更新、删除）
- 用户反馈接口（创建、获取、更新、删除）
- 分析类接口（面积分布、满意度、使用频率、安防事件类型）
