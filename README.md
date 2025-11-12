# 理财记账本 (FinanceBook)

一个基于 Flet 框架开发的跨平台个人财务管理桌面应用程序。

## 📋 项目概述

FinanceBook 是一个现代化的个人理财管理应用，提供直观的用户界面和强大的财务数据管理功能。应用采用模块化架构设计，支持用户注册登录、收支记录管理、数据统计分析等功能。

## 🏗️ 项目架构

### 架构特点

- **模块化设计**: 采用 MVC 模式，分离视图、模型和控制逻辑
- **全局状态管理**: 使用 AppState 类集中管理应用状态和用户数据
- **路由系统**: 实现了完整的页面路由管理，支持页面间导航
- **响应式布局**: 支持不同屏幕尺寸的自适应布局
- **数据库抽象**: 封装数据库操作，支持 SQLite 本地存储

### 目录结构

```
FinanceBookApp/
├── main.py                    # 应用启动入口
├── app.py                     # 主应用类，负责应用初始化和配置
├── requirements.txt           # 项目依赖
├── README.md                 # 项目说明文档
├── makefile                  # 项目构建和管理脚本
├── models/                   # 数据模型层
│   ├── __init__.py
│   ├── app_state.py          # 全局状态管理 ✅
│   ├── database.py           # 数据库管理类 ✅
│   ├── user.py              # 用户模型 ✅
│   ├── record.py            # 记录模型 ✅
│   └── category.py          # 分类模型 ✅
├── views/                    # 视图层
│   ├── __init__.py
│   ├── router.py            # 路由管理器 ✅
│   ├── welcome.py           # 欢迎页面 ✅
│   ├── login.py             # 登录页面 ✅
│   ├── register.py          # 注册页面 ✅
│   ├── dashboard.py         # 仪表板 ✅
│   ├── add_record.py        # 添加记录页面 ⚠️
│   ├── records.py           # 记录列表页面 ⚠️
│   ├── statistics.py        # 统计分析页面 ⚠️
│   └── settings.py          # 设置页面 ✅
└── components/               # 可复用组件
    ├── __init__.py
    ├── sidebar.py           # 侧边栏组件 ✅
    └── cards.py             # 卡片组件 ✅
```

## 🔧 核心技术架构

### 1. 全局状态管理 (AppState)

**实现状态**: ✅ 已完成

`AppState` 类负责管理整个应用的全局状态：

- **用户会话管理**: 维护当前登录用户信息
- **数据缓存**: 缓存用户的记录和分类数据
- **状态同步**: 确保界面与数据的实时同步
- **数据操作**: 提供统一的数据操作接口

```python
class AppState:
    def __init__(self, db: DatabaseManager, page: ft.Page):
        self.db = db
        self.page = page
        self.current_user = None
        self.records = []
        self.categories = []
        self.filtered_records = []
```

### 2. 路由系统 (Router)

**实现状态**: ✅ 已完成

基于 Flet 的路由系统，实现页面间的导航管理：

- **动态路由**: 支持带参数的路由
- **路由守卫**: 实现登录状态检查
- **页面切换**: 流畅的页面转换体验
- **历史管理**: 支持浏览器式的前进后退

支持的路由：
- `/welcome` - 欢迎页面
- `/login` - 登录页面  
- `/register` - 注册页面
- `/dashboard` - 仪表板
- `/add_record` - 添加记录
- `/records` - 记录列表
- `/statistics` - 统计分析
- `/settings` - 设置页面

```python
class Router:
    def __init__(self):
        self.page = None
        self.state = None

    def mount(self, page: ft.Page, state):
        self.page = page
        self.state = state
        page.on_route_change = self.route_change
        page.on_view_pop = self.view_pop
```

### 3. 模块化视图系统

**实现状态**: 🔄 部分完成

每个视图都是独立的模块，具有以下特性：

- **独立性**: 每个视图都是自包含的 ft.View 子类
- **数据绑定**: 与 AppState 进行数据绑定
- **事件处理**: 内置完整的用户交互处理
- **响应式设计**: 支持不同屏幕尺寸

```python
class LoginView(ft.View):
    def __init__(self, state, go):
        super().__init__(route="/login")
        self.state = state
        self.go = go
        self.page = state.page

        self.create_login_components()
        self.controls = [self.create_login_layout()]
```

## 🚀 功能特性

### 已实现功能 ✅

1. **用户系统**
   - 用户注册与登录
   - 密码加密存储
   - 会话管理

2. **仪表板**
   - 财务概览卡片
   - 最近交易列表
   - 快速操作按钮
   - 响应式布局

3. **数据管理**
   - SQLite 数据库集成
   - 用户数据隔离
   - 分类管理
   - 数据模型定义

4. **界面组件**
   - 侧边栏导航
   - 统计卡片
   - 响应式布局
   - 现代化 UI 设计

5. **统计分析**
   - 基础财务统计
   - 图表展示框架
   - 分析洞察

6. **设置页面**
   - 账户设置
   - 应用偏好
   - 数据导入导出接口

### 待实现功能 ⚠️

1. **记录管理**
   - 添加记录页面界面逻辑
   - 记录列表页面完善
   - 记录编辑和删除功能
   - 批量操作

2. **数据可视化**
   - 图表实现 (pie charts, line charts)
   - 趋势分析
   - 分类统计图表

3. **高级功能**
   - 数据导入导出 (Excel, CSV)
   - 预算管理
   - 目标设置
   - 提醒通知

4. **性能优化**
   - 数据分页
   - 延迟加载
   - 缓存机制

## 🛠️ 安装和运行

### 环境要求

- Python 3.8+
- pip 包管理器
- Make 工具 (可选，用于简化开发流程)

### 快速开始

项目提供了 Makefile 来简化常见的开发任务。推荐使用以下命令：

```bash
# 查看所有可用命令
make help

# 一键设置开发环境
make setup

# 运行应用
make run
```

### 详细安装步骤

1. **克隆项目**
```bash
git clone https://github.com/HrimeNJ/FinanceBook.git
cd FinanceBookApp
```

2. **安装依赖**
```bash
# 使用 Makefile (推荐)
make install

# 或者手动安装
pip install -r requirements.txt
```

3. **运行应用**
```bash
# 使用 Makefile (推荐)
make run

# 或者直接运行
python main.py
```

### 🔨 Makefile 使用指南

项目包含了一个完整的 Makefile，提供了便捷的开发和部署命令：

#### 基础命令

```bash
make help           # 显示所有可用命令
make install        # 安装项目依赖
make run           # 运行应用程序
make setup         # 设置开发环境
```

#### 代码质量管理

```bash
make format        # 格式化代码 (isort + black)
make lint          # 代码质量检查 (pylint)
make quick-check   # 快速代码检查 (format + lint)
make test          # 运行单元测试
```

#### 项目管理

```bash
make clean         # 清理临时文件和缓存
make backup        # 创建项目备份
make info          # 显示项目信息
make tree          # 显示项目结构
```

#### 数据库操作

```bash
make init-db       # 初始化数据库
make reset-db      # 重置数据库 (谨慎使用)
```

#### 开发工具

```bash
make dev-install   # 安装开发工具 (pre-commit, mypy 等)
make check-deps    # 检查依赖项状态
make quick-run     # 快速运行 (跳过依赖检查)
```

#### 使用示例

```bash
# 新开发者完整设置流程
git clone https://github.com/HrimeNJ/FinanceBook.git
cd FinanceBookApp
make setup          # 安装依赖和开发工具
make run           # 启动应用

# 日常开发流程
make format        # 格式化代码
make lint          # 检查代码质量
make test          # 运行测试
make run           # 启动应用

# 项目维护
make clean         # 清理缓存
make backup        # 备份项目
make info          # 查看项目信息
```

### 手动安装 (不使用 Make)

如果您的系统没有 Make 工具，可以使用以下命令：

```bash
# 安装依赖
pip install -r requirements.txt

# 安装开发工具 (可选)
pip install isort black pylint pytest

# 运行应用
python main.py

# 代码格式化 (可选)
isort . && black .

# 代码检查 (可选)
pylint **/*.py
```

## 📊 数据库设计

### 🗄️ 数据库架构

FinanceBook 使用 SQLite 作为本地数据库，提供轻量级但功能完整的数据存储方案。数据库设计遵循关系型数据库规范，确保数据的完整性和一致性。

### 📋 表结构详情

#### 🧑‍💻 users 表 - 用户信息管理
存储用户账户信息和身份验证数据

| 字段名 | 数据类型 | 约束条件 | 说明 |
|--------|---------|---------|------|
| `user_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 用户唯一标识符 |
| `username` | TEXT | UNIQUE, NOT NULL | 用户名，用于登录 |
| `password_hash` | TEXT | NOT NULL | 加密后的密码哈希值 |
| `email` | TEXT | UNIQUE, NOT NULL | 用户邮箱地址 |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 账户创建时间 |
| `last_login` | TIMESTAMP | NULLABLE | 最后登录时间 |

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

#### 🏷️ categories 表 - 分类管理
管理收入和支出的分类信息，支持层级结构

| 字段名 | 数据类型 | 约束条件 | 说明 |
|--------|---------|---------|------|
| `category_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 分类唯一标识符 |
| `name` | TEXT | NOT NULL | 分类名称 (如：餐饮、交通) |
| `parent_id` | INTEGER | FOREIGN KEY, NULLABLE | 父分类ID，支持子分类 |
| `is_active` | BOOLEAN | DEFAULT 1 | 分类状态 (1:启用, 0:禁用) |

```sql
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (parent_id) REFERENCES categories (category_id)
);
```

#### 📝 records 表 - 财务记录
存储用户的所有收入和支出记录

| 字段名 | 数据类型 | 约束条件 | 说明 |
|--------|---------|---------|------|
| `record_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 记录唯一标识符 |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | 关联的用户ID |
| `amount` | REAL | NOT NULL, > 0 | 交易金额 |
| `record_type` | TEXT | CHECK ('income', 'expense') | 记录类型：收入或支出 |
| `category_id` | INTEGER | FOREIGN KEY, NOT NULL | 关联的分类ID |
| `note` | TEXT | NULLABLE | 交易备注说明 |
| `date` | DATE | NOT NULL | 交易日期 |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 记录创建时间 |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 最后修改时间 |

```sql
CREATE TABLE records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    date TIMESTAMP NOT NULL,
    record_type TEXT NOT NULL CHECK (record_type IN ('income', 'expense')),
    note TEXT,
    category_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (category_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```

### 🔗 数据关系图

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│    users    │       │   records    │       │ categories  │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ user_id (PK)│◄──────┤ user_id (FK) │       │category_id  │
│ username    │       │ record_id(PK)│       │(PK)         │
│ email       │       │ amount       │       ├─────────────┤
│ ...         │       │ record_type  │   ┌───┤ name        │
└─────────────┘       │ note         │   │   │ parent_id   │
                      │ date         │   │   │ is_active   │
                      │ category_id  │───┘   └─────────────┘
                      │ (FK)         │            │
                      └──────────────┘            │
                                                  └──┐ 自关联
                                                     │ (子分类)
                                                     ▼
```

### 💾 数据库特性

- **🔒 数据隔离**: 每个用户只能访问自己的财务记录
- **🌳 分层分类**: 支持多级分类结构 (如：生活费用 → 餐饮 → 外卖)
- **📈 完整性**: 外键约束确保数据一致性
- **🕐 时间追踪**: 自动记录创建和修改时间
- **🔍 索引优化**: 关键字段建立索引，提升查询性能

### 🚀 默认数据

系统会自动初始化以下默认分类：

**📊 支出分类**
- 🍽️ 餐饮、🚗 交通、🛍️ 购物、🎬 娱乐
- 🏥 医疗、📚 教育、🏠 住房、📦 其他支出

**💰 收入分类**
- 💼 工资、🎁 奖金、📈 投资、💎 其他收入

## 🎯 开发计划

### 🔄 待完成功能

#### 核心功能模块
- [ ] **添加记录页面** - 完善收支记录的添加和编辑界面
- [ ] **记录列表管理** - 实现记录的查看、编辑、删除和搜索功能
- [ ] **数据可视化** - 集成图表库，实现饼图、折线图等数据展示
- [ ] **数据验证** - 完善表单验证和错误处理机制

#### 高级功能
- [ ] **数据导入导出** - 支持 Excel、CSV 格式的数据导入导出
- [ ] **预算管理** - 设置月度/年度预算并跟踪执行情况
- [ ] **统计分析** - 深度财务分析和趋势预测
- [ ] **主题切换** - 支持明暗主题和自定义配色

#### 用户体验
- [ ] **搜索过滤** - 多条件搜索和智能过滤
- [ ] **数据分页** - 大数据量的分页加载
- [ ] **快捷操作** - 键盘快捷键和批量操作
- [ ] **提醒通知** - 预算超支提醒和定期记账提醒

#### 扩展功能
- [ ] **云同步** - 多设备数据同步 (未来版本)
- [ ] **移动端适配** - 响应式设计优化
- [ ] **插件系统** - 支持第三方功能扩展
- [ ] **多语言支持** - 国际化和本地化
- [ ] **API接口** - 开放API供第三方应用集成

---

### 🚧 当前开发状态

✅ **已完成**: 基础架构、用户系统、仪表板界面、数据库设计  
🔄 **进行中**: 记录管理功能、数据可视化  
⏳ **计划中**: 高级统计分析、扩展功能

### 开发规范

使用 Makefile 命令来保持代码质量：

```bash
# 提交前检查
make format        # 格式化代码
make lint          # 检查代码质量
make test          # 运行测试

# 或者一键检查
make quick-check
```

## 📝 技术说明

### 状态管理流程
```
User Action → View → AppState → Database → AppState → View Update
```

### 路由导航流程
```
User Click → Router.route_change → View Cleanup → New View Mount → UI Update
```

### 数据流向
```
Database ↔ AppState ↔ Views ↔ User Interface
```

### 开发工作流程
```
Code → make format → make lint → make test → Commit → Push
```

## 🐛 问题反馈

如果您发现任何问题或有功能建议，请在 [Issues](../../issues) 页面提交。

### 常见问题

1. **启动失败**: 运行 `make check-deps` 检查依赖项
2. **数据库错误**: 运行 `make init-db` 重新初始化数据库
3. **导入错误**: 确保在项目根目录运行命令

## 🔧 故障排除

```bash
# 检查环境
make info
make check-deps

# 清理并重新安装
make clean
make install

# 重置数据库
make reset-db
make init-db
```

---

**注意**: 当前版本为开发版本，部分功能仍在完善中。建议在生产环境使用前进行充分测试。