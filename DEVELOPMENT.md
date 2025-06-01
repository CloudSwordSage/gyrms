# GoldenYearsManager 开发文档

## 项目概述
GoldenYearsManager是一个养老院管理系统，包含前端(Vue 3)和后端(FastAPI)两部分。

## 技术栈
### 前端
- Vue 3 + TypeScript
- Vite构建工具
- Pinia状态管理
- Vue Router

### 后端
- Python 3.x
- FastAPI框架
- SQLAlchemy ORM
- MySQL数据库
- JWT认证

## 开发环境配置

### 前端
1. 安装Node.js 16+
2. 安装依赖：
```bash
cd GoldenYearsManager
npm install
```
3. 开发模式运行：
```bash
npm run dev
```

### 后端
```
docker-compose up -d
```
注意修改main.py中的跨域配置

## API文档
后端API使用FastAPI自动生成文档：
- 开发环境: http://localhost:8000/docs
- Swagger UI: http://localhost:8000/redoc

主要API模块：
- 认证(auth)
- 用户管理(users)
- 老人信息(persons)
- 护理计划(care_plans)
- 护理记录(care)

## 部署指南
1. 生产环境建议使用Docker部署
2. 后端Dockerfile已配置
3. 前端构建：
```bash
npm run build
```
4. 配置Nginx反向代理

## 管理员账号
默认管理员账号：
- 用户名: admin
- 密码: AdminGyRmS.114514
