# main.py
from fastapi import FastAPI
from routers import user, device, analytics,usage_log, security_event, feedback
app = FastAPI(title="Smart Home API")

app.include_router(user.router)
app.include_router(device.router)
app.include_router(analytics.router, prefix="/analytics")
app.include_router(usage_log.router)
app.include_router(usage_log.router)
app.include_router(security_event.router)
app.include_router(feedback.router)
# #  # 在 main.py 末尾临时加--运行一次后不再重复运行：
# from database import engine
# from models import tables
# tables.Base.metadata.drop_all(bind=engine)   # 清空表
# tables.Base.metadata.create_all(bind=engine) # 重新建表



