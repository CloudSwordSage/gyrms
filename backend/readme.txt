GYRMS 后端项目说明

本项目是一个Python后端服务，用于管理GYRMS(养老院管理系统)的API和业务逻辑。

主要目录结构：

1. api/ - API路由处理
   - auth.py - 认证相关API
   - care.py - 护理相关API
   - care_plans.py - 护理计划API
   - persons.py - 人员管理API
   - reminders.py - 提醒功能API
   - users.py - 用户管理API

2. models/ - 数据库模型
   - base.py - 基础模型类
   - care.py - 护理记录模型
   - care_plan.py - 护理计划模型
   - health.py - 健康记录模型
   - person.py - 人员模型
   - reminder.py - 提醒模型
   - user.py - 用户模型

3. schema/ - 数据验证模式
   - 各文件对应models/中的模型验证

4. services/ - 业务逻辑
   - 各文件实现核心业务功能

5. utils/ - 工具函数
   - database.py - 数据库连接
   - security.py - 安全相关
   - init_admin.py - 初始化管理员

6. config/ - 配置
   - config.py - 应用配置

7. alembic/ - 数据库迁移
   - versions/ - 迁移脚本

根目录重要文件：
- main.py - 主程序入口
- Dockerfile - Docker构建文件
- docker-compose.yml - Docker编排
- requirements.txt - Python依赖
- .env - 环境变量
- start.sh - 启动脚本
- create_user.py - 用户创建工具
- sqlcreate.sh - 数据库创建脚本
