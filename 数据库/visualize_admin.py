# 文件：visualize_admin.py
# 功能：管理员视角，全局图表 G1~G7（不依赖用户ID）

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pandas as pd

matplotlib.use('TKAgg')
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

API = "http://127.0.0.1:8000/analytics"

def plot_G1_device_usage_and_hourly():
    print("\U0001F4CA G1：设备频率 + 每小时趋势")
    freq = requests.get(f"{API}/device-usage-count").json()
    hour = requests.get(f"{API}/hourly-usage").json()

    df1 = pd.DataFrame(freq)
    df2 = pd.DataFrame(hour)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=df1["device_name"], y=df1["usage_count"])
    plt.title("G1：设备使用频率统计")
    plt.tight_layout()
    plt.savefig("G1_device_freq.png")
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.lineplot(x=df2["hour"], y=df2["usage_count"], marker="o")
    plt.title("G1：每小时总用电趋势")
    plt.tight_layout()
    plt.savefig("G1_hourly_usage.png")
    plt.close()

def plot_G2_device_pair_correlation():
    print("\U0001F4CA G2：设备同时使用频率")
    pairs = requests.get(f"{API}/frequent-pairs").json()
    df = pd.DataFrame(pairs)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df["count"], y=df["device_pair"])
    plt.title("G2：设备配对共用频率")
    plt.tight_layout()
    plt.savefig("G2_frequent_pairs.png")
    plt.close()

def plot_G3_area_vs_usage_scatter():
    print("\U0001F4CA G3：面积 vs 用电")
    df = pd.DataFrame(requests.get(f"{API}/area-usage").json())
    plt.figure(figsize=(6, 5))
    sns.regplot(x="house_area", y="usage_count", data=df, scatter_kws={'s':60})
    plt.title("G3：房屋面积 vs 用电次数")
    plt.tight_layout()
    plt.savefig("G3_area_vs_usage.png")
    plt.close()

def plot_G4_device_avg_duration():
    print("\U0001F4CA G4：平均使用时长")
    df = pd.DataFrame(requests.get(f"{API}/device-average-duration").json())
    plt.figure(figsize=(8, 5))
    sns.barplot(x="avg_duration", y="device_name", data=df)
    plt.title("G4：各设备平均使用时长")
    plt.tight_layout()
    plt.savefig("G4_avg_duration.png")
    plt.close()

def plot_G5_feedback_trend():
    print("\U0001F4CA G5：满意度趋势")
    df = pd.DataFrame(requests.get(f"{API}/feedback-trend").json())
    plt.figure(figsize=(8, 4))
    sns.lineplot(x="date", y="avg_rating", data=df, marker='o')
    plt.title("G5：每日平均评分趋势")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("G5_feedback_trend.png")
    plt.close()

def plot_G6_security_events():
    print("\U0001F4CA G6：安防事件统计")
    raw = requests.get(f"{API}/security-events-summary").json()
    df = pd.DataFrame(raw).T.fillna(0)
    df.index.name = 'date'
    df.sort_index(inplace=True)
    df.plot(kind="bar", stacked=True, figsize=(10, 6))
    plt.title("G6：每日安防事件堆叠图")
    plt.tight_layout()
    plt.savefig("G6_security_events.png")
    plt.close()

def plot_G7_area_vs_usage_bar():
    print("\U0001F4CA G7：面积 vs 用电次数")
    df = pd.DataFrame(requests.get(f"{API}/area-usage").json())
    plt.figure(figsize=(8, 5))
    sns.barplot(x="house_area", y="usage_count", data=df)
    plt.title("G7：不同面积房屋用电统计")
    plt.tight_layout()
    plt.savefig("G7_area_usage_bar.png")
    plt.close()

def plot_G8_area_device_duration():
    print("📊 G8：面积 vs 设备（日均时长）")
    # df = pd.DataFrame(requests.get(f"{API}/area-device-usage").json())
    resp = requests.get(f"{API}/area-device-usage")
    print("【DEBUG】接口响应状态：", resp.status_code)
    print("【DEBUG】接口原始返回：", resp.text)
    df = pd.DataFrame(resp.json())

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x="house_area",
        y="device_name",
        size="avg_duration",
        sizes=(20, 400),
        legend="brief",
        alpha=0.7
    )
    plt.title("G8：房屋面积 vs 设备（日均使用时长）")
    plt.xlabel("房屋面积")
    plt.ylabel("设备名称")
    plt.tight_layout()
    plt.savefig("G8_area_device_duration.png")
    plt.close()

def plot_G9_area_device_freq():
    print("📊 G9：面积 vs 设备（日均频次）")
    df = pd.DataFrame(requests.get(f"{API}/area-device-usage").json())
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x="house_area",
        y="device_name",
        size="avg_count",
        sizes=(20, 400),
        legend="brief",
        alpha=0.7
    )
    plt.title("G9：房屋面积 vs 设备（日均使用频次）")
    plt.xlabel("房屋面积")
    plt.ylabel("设备名称")
    plt.tight_layout()
    plt.savefig("G9_area_device_frequency.png")
    plt.close()


if __name__ == "__main__":
    plot_G1_device_usage_and_hourly()
    plot_G2_device_pair_correlation()
    plot_G3_area_vs_usage_scatter()
    plot_G4_device_avg_duration()
    plot_G5_feedback_trend()
    plot_G6_security_events()
    plot_G7_area_vs_usage_bar()
    plot_G8_area_device_duration()
    plot_G9_area_device_freq()

    print("✅ 管理员视角图表生成完毕")
