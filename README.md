# 理财记账本 (FinanceBook)

一个基于 Flet 框架开发的跨平台个人财务管理桌面应用程序。

## 📋 项目概述

FinanceBook 是一个现代化的个人理财管理应用，提供直观的用户界面和强大的财务数据管理功能。应用采用模块化架构设计，支持用户注册登录、收支记录管理、数据统计分析、数据可视化图表等功能。

## 🏗️ 项目架构

### 架构特点

- **模块化设计**: 采用 MVC 模式，分离视图、模型和控制逻辑
- **全局状态管理**: 使用 AppState 类集中管理应用状态和用户数据
- **路由系统**: 实现了完整的页面路由管理，支持页面间导航
- **响应式布局**: 支持不同屏幕尺寸的自适应布局
- **数据库抽象**: 封装数据库操作，支持 SQLite 本地存储
- **数据可视化**: 集成图表组件，支持饼图和折线图展示

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
│   ├── category.py          # 分类模型 ✅
│   └── export.py            # 数据导出模块 ✅
├── views/                    # 视图层
│   ├── __init__.py
│   ├── router.py            # 路由管理器 ✅
│   ├── welcome.py           # 欢迎页面 ✅
│   ├── login.py             # 登录页面 ✅
│   ├── register.py          # 注册页面 ✅
│   ├── dashboard.py         # 仪表板 ✅
│   ├── add_record.py        # 添加记录页面 ✅
│   ├── records.py           # 记录列表页面 ⚠️
│   ├── statistics.py        # 统计分析页面 ✅
│   └── settings.py          # 设置页面 ✅
└── components/               # 可复用组件
    ├── __init__.py
    ├── sidebar.py           # 侧边栏组件 ✅
    └── cards.py             # 卡片组件 ✅
```

## 🚀 功能特性

### 已实现功能 ✅

1. **用户系统**
   - 用户注册与登录
   - 密码加密存储 (SHA-256)
   - 会话管理
   - 用户数据隔离

2. **记录管理**
   - 添加收入/支出记录
   - 记录分类管理
   - 日期选择和备注
   - 表单验证

3. **仪表板**
   - 财务概览卡片
   - 实时统计数据展示
   - 最近交易列表
   - 快速操作按钮

4. **统计分析** 
   - 收支对比和变化率计算
   - 最近7天收支趋势折线图
   - 最大支出分类分析
   - 日均支出统计

5. **数据可视化** 
   - 支出分类饼图 (PieChart)
   - 收支趋势折线图 (LineChart)

6. **数据导出** 
   - JSON 格式导出
   - Excel 格式导出 (.xlsx)

7. **设置页面**
   - 账户设置
   - 主题切换 (明暗模式)
   - 数据导入导出功能
   - 用户信息展示

### 待实现功能 ⚠️

1. **记录管理增强**
   - 记录编辑和删除功能
   - 批量操作
   - 高级搜索和过滤

2. **高级功能**
   - 数据导入 (Excel, CSV)
   - 预算管理和跟踪
   - 目标设置
   - 提醒通知
   - 定期报表生成

3. **数据分析**
   - 月度对比分析
   - 年度财务报告
   - 消费习惯分析
   - AI 智能建议

4. **性能优化**
   - 数据分页加载
   - 缓存机制
   - 延迟加载优化

## 🛠️ 安装和运行

### 环境要求

- Python 3.8+
- pip 包管理器
- Make 工具 (可选，用于简化开发流程)

### 依赖项

```bash
# 核心依赖
flet>=0.21.0

# 可选依赖 (用于 Excel 导出)
openpyxl>=3.1.0
```

### 快速开始

项目提供了 Makefile 来简化常见的开发任务。推荐使用以下命令:

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

# 安装可选依赖 (Excel 导出功能)
pip install openpyxl
```

3. **运行应用**
```bash
# 使用 Makefile (推荐)
make run

# 或者直接运行
python main.py
```

## 📊 数据库设计

### 🗄️ 数据库架构

FinanceBook 使用 SQLite 作为本地数据库，提供轻量级但功能完整的数据存储方案。

### 📋 表结构详情

#### 🧑‍💻 users 表 - 用户信息管理

| 字段名 | 数据类型 | 约束条件 | 说明 |
|--------|---------|---------|------|
| `user_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 用户唯一标识符 |
| `username` | TEXT | UNIQUE, NOT NULL | 用户名，用于登录 |
| `password_hash` | TEXT | NOT NULL | 加密后的密码哈希值 |
| `email` | TEXT | UNIQUE, NOT NULL | 用户邮箱地址 |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 账户创建时间 |
| `last_login` | TIMESTAMP | NULLABLE | 最后登录时间 |

#### 🏷️ categories 表 - 分类管理

| 字段名 | 数据类型 | 约束条件 | 说明 |
|--------|---------|---------|------|
| `category_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 分类唯一标识符 |
| `name` | TEXT | NOT NULL | 分类名称 |
| `parent_id` | INTEGER | FOREIGN KEY, NULLABLE | 父分类ID |
| `is_active` | BOOLEAN | DEFAULT 1 | 分类状态 |

#### 📝 records 表 - 财务记录

| 字段名 | 数据类型 | 约束条件 | 说明 |
|--------|---------|---------|------|
| `record_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 记录唯一标识符 |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | 关联的用户ID |
| `amount` | REAL | NOT NULL, > 0 | 交易金额 |
| `record_type` | TEXT | CHECK ('income', 'expense') | 记录类型 |
| `category_id` | INTEGER | FOREIGN KEY, NOT NULL | 关联的分类ID |
| `note` | TEXT | NULLABLE | 交易备注 |
| `date` | DATE | NOT NULL | 交易日期 |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新时间 |

## 📈 统计功能说明

### 周期统计

支持多种时间周期的数据统计:
- **周统计**: 本周 vs 上周
- **月统计**: 本月 vs 上月  
- **季度统计**: 本季度 vs 上季度
- **年统计**: 本年 vs 上年

### 统计指标

- 总收入和变化率
- 总支出和变化率
- 净储蓄和变化率
- 最大支出分类
- 日均支出
- 交易笔数统计

### 数据可视化

1. **支出分类饼图**
   - 展示各分类支出占比
   - 显示金额和百分比
   - 交互式图表

2. **收支趋势折线图**
   - 显示最近7天收支趋势
   - 双线对比展示
   - 自动日期标签

## 💾 数据导出功能

### JSON 导出

导出完整的结构化数据:
```json
{
  "export_time": "2024-01-15T10:30:00",
  "user": {...},
  "categories": [...],
  "records": [...],
  "summary": {...}
}
```

### Excel 导出

生成专业的多工作表 Excel 文件:
- **数据汇总**: 用户信息和财务统计
- **记账记录**: 完整的交易明细
- **分类列表**: 所有分类信息

导出文件保存位置: `./FinanceBookExports/`

## 🔨 Makefile 使用指南

### 基础命令

```bash
make help           # 显示所有可用命令
make install        # 安装项目依赖
make run           # 运行应用程序
make setup         # 设置开发环境
```

### 代码质量管理

```bash
make format        # 格式化代码 (isort + black)
make lint          # 代码质量检查 (pylint)
make quick-check   # 快速代码检查
make test          # 运行单元测试
```

### 项目管理

```bash
make clean         # 清理临时文件和缓存
make backup        # 创建项目备份
make info          # 显示项目信息
```

### 数据库操作

```bash
make init-db       # 初始化数据库
make reset-db      # 重置数据库 (谨慎使用)
```

## 🔄 开发进度

### 功能完成度

| 功能模块 | 完成度 | 状态 |
|---------|-------|------|
| 用户系统 | 100% | ✅ |
| 仪表板 | 100% | ✅ |
| 记录管理 | 80% | ✅ |
| 统计分析 | 90% | ✅ |
| 数据可视化 | 85% | ✅ |
| 数据导出 | 100% | ✅ |
| 设置功能 | 85% | ✅ |


### 代码提交前检查

```bash
make format        # 格式化代码
make lint          # 检查代码质量
```
---

**注意**: 当前版本为开发版本，建议在生产环境使用前进行充分测试。