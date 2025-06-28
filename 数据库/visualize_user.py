# 文件：visualize_user.py
# 功能：用户视角，全套 U1–U4 + 用户版 G1–G7

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pandas as pd

matplotlib.use('TKAgg')
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

API = "http://127.0.0.1:8000/analytics"
def safe_get_json(url, label=""):
    """安全获取JSON数据，若失败或为空则打印警告"""
    try:
        response = requests.get(url)
        if not response.ok:
            print(f"⚠️ [{label}] 请求失败：{response.status_code}")
            return None
        data = response.json()
        if not data:
            print(f"⚠️ [{label}] 返回数据为空")
            return None
        return data
    except Exception as e:
        print(f"❌ [{label}] 请求或解析失败：{e}")
        return None


# ------------------ 用户版 G 图（G1–G7） ------------------

def plot_G1_user_hourly(user_id):
    print("📊 G1（用户）：每小时使用趋势")
    data = safe_get_json(f"{API}/user-hourly-usage/{user_id}", label="G1")
    if not data:
        return
    df = pd.DataFrame(data)
    if df.empty: return
    plt.figure(figsize=(8, 4))
    sns.lineplot(x="hour", y="usage_count", data=df, marker="o")
    plt.title(f"用户{user_id} 每小时使用趋势")
    plt.xlabel("小时")
    plt.ylabel("使用次数")
    plt.tight_layout()
    plt.savefig(f"G1_user{user_id}_hourly.png")
    plt.close()

def plot_G2_user_pair(user_id):
    print("📊 G2（用户）：设备同时使用频率")
    data = safe_get_json(f"{API}/user-frequent-pairs/{user_id}", label="G2")
    if not data:
        return
    df = pd.DataFrame(data)
    if df.empty: return
    plt.figure(figsize=(10, 5))
    sns.barplot(x="count", y="device_pair", data=df)
    plt.title(f"用户{user_id} 设备配对共用频率")
    plt.tight_layout()
    plt.savefig(f"G2_user{user_id}_frequent_pairs.png")
    plt.close()

def plot_G3_user_avg_duration(user_id):
    print(" G3（用户）：设备平均使用时长")
    data = safe_get_json(f"{API}/user-device-average-duration/{user_id}", label="G3")
    if not data:
        return
    df = pd.DataFrame(data)
    if df.empty: return
    plt.figure(figsize=(8, 5))
    sns.barplot(x="avg_duration", y="device_name", data=df)
    plt.title(f"用户{user_id} 各设备平均使用时长")
    plt.tight_layout()
    plt.savefig(f"G3_user{user_id}_avg_duration.png")
    plt.close()

def plot_G4_user_feedback(user_id):
    print("G4（用户）：满意度趋势")
    data = safe_get_json(f"{API}/user-feedback-trend/{user_id}", label="G4")
    if not data:
        return
    df = pd.DataFrame(data)
    if df.empty: return
    plt.figure(figsize=(8, 4))
    sns.lineplot(x="date", y="avg_rating", data=df, marker="o")
    plt.title(f"用户{user_id} 满意度趋势")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"G4_user{user_id}_feedback_trend.png")
    plt.close()

def plot_G5_user_security(user_id):
    print("📊 G5（用户）：安防事件分布图（彩色散点）")
    raw = safe_get_json(f"{API}/user-security-events-summary/{user_id}", label="G5")
    if not raw:
        return

    records = []
    for date_str, events in raw.items():
        for event_type, count in events.items():
            for _ in range(count):
                records.append({"date": date_str, "event_type": event_type})

    if not records:
        print(f"⚠️ G5：用户{user_id} 无安防事件记录")
        return

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="date", y="event_type", hue="event_type", s=80, alpha=0.8)
    plt.title(f"G5：用户{user_id} 安防事件分布图")
    plt.xlabel("日期")
    plt.ylabel("事件类型")
    plt.xticks(rotation=45)
    plt.legend(title="事件类型")
    plt.tight_layout()
    plt.savefig(f"G5_user{user_id}_security_events_scatter.png")
    plt.close()

# ------------------ 用户个性化图 U1–U4 ------------------
def plot_U1_user_device_usage(user_id):
    print("📊 U1：设备使用频率")
    df = pd.DataFrame(requests.get(f"{API}/user-device-usage/{user_id}").json())
    if df.empty: return
    plt.figure(figsize=(8, 5))
    sns.barplot(x="usage_count", y="device_name", data=df)
    plt.title(f"U1：用户{user_id} 设备使用频率")
    plt.tight_layout()
    plt.savefig(f"U1_user{user_id}_device_usage.png")
    plt.close()

def plot_U2_user_day_gantt(user_id, date_str):
    print(f"📊 U2（日）：{date_str} 甘特图")
    df = pd.DataFrame(requests.get(f"{API}/user-device-timeline-by-date/{user_id}?date={date_str}").json())
    if df.empty: return
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['start_hour'] = df['start_time'].dt.hour + df['start_time'].dt.minute / 60
    df['end_hour'] = df['start_hour'] + df['duration'] / 60
    device_map = {n: i for i, n in enumerate(df['device_name'].unique())}
    plt.figure(figsize=(12, 6))
    for _, r in df.iterrows():
        plt.hlines(y=device_map[r['device_name']], xmin=r['start_hour'], xmax=r['end_hour'], linewidth=4)
    plt.yticks(list(device_map.values()), list(device_map.keys()))
    plt.xlim(0, 24)
    plt.title(f"U2（日）：用户{user_id} 在 {date_str} 的设备使用甘特图")
    plt.tight_layout()
    plt.savefig(f"U2_user{user_id}_{date_str}_gantt.png")
    plt.close()

def plot_U3_device_daily_duration(user_id, device_name):
    print(f"📊 U3：{device_name} 每日使用时长")
    df = pd.DataFrame(requests.get(f"{API}/user-device-daily-duration/{user_id}?device_name={device_name}").json())
    if df.empty: return
    plt.figure(figsize=(10, 5))
    sns.lineplot(x="date", y="total_minutes", data=df, marker="o")
    plt.title(f"U3：用户{user_id} 设备“{device_name}”每日时长")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"U3_user{user_id}_{device_name}_daily.png")
    plt.close()

def plot_U4_user_top_devices(user_id):
    print("📊 U4：TOP3 设备占比")
    df = pd.DataFrame(requests.get(f"{API}/user-top-devices/{user_id}").json())
    if df.empty: return
    plt.figure(figsize=(6, 6))
    plt.pie(df['percent'], labels=df['device_name'], autopct='%1.1f%%', startangle=140)
    plt.title(f"U4：用户{user_id} TOP3 设备占比")
    plt.tight_layout()
    plt.savefig(f"U4_user{user_id}_top3.png")
    plt.close()


# ------------------ 主流程 ------------------

if __name__ == "__main__":
    user_id = int(input("请输入用户ID："))
    date_str = input("请输入日期 (YYYY-MM-DD)：")
    device_name = input("请输入设备名称：")

    # U 与 G 用户版并行生成
    plot_U1_user_device_usage(user_id)
    plot_U2_user_day_gantt(user_id, date_str)
    plot_U3_device_daily_duration(user_id, device_name)
    plot_U4_user_top_devices(user_id)

    plot_G1_user_hourly(user_id)
    plot_G2_user_pair(user_id)
    plot_G3_user_avg_duration(user_id)
    plot_G4_user_feedback(user_id)
    plot_G5_user_security(user_id)

    print("✅ 所有用户视角图表（U1–U4 + G1–G7）生成完毕")
