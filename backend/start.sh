#!/bin/bash

# 创建数据库和用户
python create_user.py

# 执行数据库迁移
alembic upgrade head

# 初始化管理员
python -m utils.init_admin

# 启动应用
uvicorn main:app --host 0.0.0.0 --port 8000
