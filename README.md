# GoldenYearsManager项目README

## 一、项目简介
GoldenYearsManager是一个养老院管理系统，涵盖了后端与前端的开发。后端采用Python的FastAPI框架进行开发，搭配SQLAlchemy ORM与MySQL数据库进行数据存储与操作；前端使用Vue 3 + TypeScript构建用户界面，借助Element - Plus进行UI设计，利用Pinia进行状态管理。

## 二、安装说明
1. **后端依赖安装**：
    - 进入`backend`目录，在命令行中执行`cd backend`。
    - 安装项目所需依赖，运行`pip install -r requirements.txt`。
2. **前端依赖安装**：
    - 进入`GoldenYearsManager`目录，执行`cd GoldenYearsManager`。
    - 安装前端依赖，运行`npm install`。

## 三、使用方法
1. **启动后端服务**：可使用`docker-compose up -d`启动后端服务，注意修改`main.py`中的跨域配置。后端API文档在开发环境可通过http://localhost:8000/docs访问，Swagger UI可通过http://localhost:8000/redoc访问。
2. **启动前端服务**：在`GoldenYearsManager`目录下，执行`npm run dev`。
3. **访问应用**：在浏览器中输入前端启动后的地址（通常为http://localhost:3000，具体端口可在前端启动日志中查看），即可访问应用。

## 四、项目结构
1. **后端**：
    - `api`目录：包含各种API接口的定义，如`auth.py`负责认证相关接口，`care_plans.py`负责护理计划相关接口等。
    - `config`目录：存放项目配置文件，如`config.py`。
    - `models`目录：定义数据库模型，如`user.py`定义用户模型，`care_plan.py`定义护理计划模型等。
    - `schema`目录：用于数据验证与序列化，如`user.py`定义用户相关的数据验证模式。
    - `services`目录：包含业务逻辑处理函数，如`users.py`处理用户相关业务逻辑。
    - `utils`目录：存放一些工具函数，如`database.py`处理数据库连接相关工具函数。
2. **前端**：
    - `src/api`目录：负责与后端API进行交互，如`auth.ts`处理认证相关API请求。
    - `src/components`目录：存放各种Vue组件，如`PersonForm.vue`用于人员信息表单。
    - `src/router`目录：定义前端路由，如`index.ts`配置应用的路由规则。
    - `src/stores`目录：用于状态管理，如`auth.ts`管理认证相关状态。
    - `src/views`目录：存放各种视图组件，如`LoginView.vue`为登录视图，`CarePlanListView.vue`为护理计划列表视图等。

## 五、贡献指南
1. **分支管理**：暂未提及明确分支管理策略，建议遵循常规Git分支管理，如主分支用于稳定版本，开发分支用于日常开发等。
2. **代码规范**：后端遵循PEP8代码规范，前端遵循ESLint结合Vue官方推荐的代码规范。
3. **提交说明**：提交代码时，请提供清晰的提交说明，描述本次提交的主要内容与目的。

## 六、许可证
本项目使用GNU General Public License Version 3，详情请查看`LICENSE`文件。
