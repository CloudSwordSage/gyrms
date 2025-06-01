# GYRMS 养老院管理系统 - 安装及使用指南

## 第五章 安装及使用

### 1. 环境要求

#### 1.1 硬件要求
- 最低配置：2核CPU/4GB内存/50GB硬盘
- 推荐配置：4核CPU/8GB内存/100GB硬盘

#### 1.2 软件要求
**后端服务：**
- Python 3.7+
- MySQL 5.7+ 或 PostgreSQL 12+
- Docker (可选，用于容器化部署)

**前端服务：**
- Node.js 16+
- npm 8+ 或 yarn 1.22+

### 2. 安装过程

#### 2.1 后端服务安装
1. 克隆项目仓库
2. 进入backend目录：
   ```bash
   cd backend
   ```
3. 创建Python虚拟环境：
   ```bash
   python -m venv venv
   ```
4. 激活虚拟环境：
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
5. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
6. 配置环境变量：
   - 复制.env.example为.env
   - 修改数据库连接等配置

#### 2.2 前端服务安装
1. 进入GoldenYearsManager目录：
   ```bash
   cd GoldenYearsManager
   ```
2. 安装依赖：
   ```bash
   npm install
   ```
3. 配置环境变量：
   - 复制.env.example为.env
   - 修改API基础URL等配置

### 3. 启动流程

#### 3.1 后端服务启动
1. 启动数据库服务
2. 执行数据库迁移：
   ```bash
   alembic upgrade head
   ```
3. 启动服务：
   ```bash
   uvicorn main:app --reload
   ```
   - 或使用Docker：
     ```bash
     docker-compose up -d
     ```

#### 3.2 前端服务启动
1. 开发模式：
   ```bash
   npm run dev
   ```
2. 生产构建：
   ```bash
   npm run build
   ```

### 4. 典型使用流程

1. **系统初始化**
   - 访问前端页面
   - 使用默认管理员账号登录(admin/admin123)
   - 修改默认密码

2. **基础配置**
   - 添加养老院工作人员账号
   - 添加老人基本信息
   - 配置护理项目

3. **日常使用**
   - 制定护理计划
   - 记录护理执行情况
   - 查看提醒事项
   - 生成各类报表

4. **系统维护**
   - 定期备份数据库
   - 更新系统版本
   - 监控系统运行状态

### 5. 注意事项
1. 首次使用请务必修改默认密码
2. 生产环境请勿使用--reload参数
3. 定期检查数据库备份是否正常
4. 更新版本前请先备份数据
