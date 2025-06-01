GoldenYearsManager 项目说明

本项目是一个养老院管理系统前端，基于Vue.js框架开发，主要功能包括：
- 用户认证与管理
- 老人信息管理
- 护理计划制定与跟踪
- 护理记录管理
- 提醒事项管理

项目文件结构说明：

1. 配置文件
- .env: 环境变量配置
- tsconfig.*.json: TypeScript配置
- vite.config.ts: Vite构建配置
- package.json: 项目依赖配置

2. 主应用文件
- src/main.ts: 应用入口文件
- src/App.vue: 根组件
- src/router/index.ts: 路由配置

3. API接口
- src/api/*.ts: 各模块API接口定义
  - auth.ts: 认证相关API
  - user.ts: 用户管理API
  - person.ts: 老人信息API
  - carePlan.ts: 护理计划API
  - care.ts: 护理记录API
  - reminder.ts: 提醒事项API

4. 组件
- src/components/: 可复用组件
  - person/PersonForm.vue: 老人信息表单组件

5. 视图页面
- src/views/: 各功能模块页面
  - auth/: 认证相关页面
  - user/: 用户管理页面
  - person/: 老人信息管理页面
  - care-plans/: 护理计划管理页面
  - care-records/: 护理记录管理页面
  - reminder/: 提醒事项管理页面

6. 工具类
- src/utils/encrypt.ts: 加密工具
- src/stores/auth.ts: Pinia状态管理

7. 静态资源
- public/: 公共静态资源
- src/assets/: 应用静态资源
