# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从 .env 文件中读取数据库连接地址
DATABASE_URL = os.getenv("DATABASE_URL")

#  创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

#  创建数据库会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建模型基类
Base = declarative_base()

# 提供 FastAPI 路由依赖注入的 get_db() 方法
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
