# 生鲜仓储系统后端原型（Fresh Warehouse Backend Prototype）

## 1. 项目简介

本项目是一个用于演示的生鲜仓储 / 供应链管理系统后端原型，聚焦库存管理闭环的核心流程。  
当前版本主要用于技术验证与流程演示，帮助团队快速搭建并验证基础仓储能力。

技术栈：

- FastAPI
- SQLModel
- SQLite

## 2. 当前已实现模块

当前后端已实现以下核心模块：

1. 商品管理（`/products`）
2. 仓库管理（`/warehouses`）
3. 库存查询（`/inventory`）
4. 入库操作（`/inbound`）
5. 出库操作（`/outbound`）
6. 库存流水（`/stock-movements`）

业务上支持：

- 记录商品与仓库基础信息
- 查询各商品在不同仓库的库存
- 入库自动增加库存并记录流水
- 出库自动扣减库存并记录流水
- 出库时校验库存不足并返回错误

## 3. 项目结构

```text
fresh-warehouse-demo/
├── backend/
│   ├── main.py                 # FastAPI 应用入口
│   ├── database.py             # 数据库引擎、会话、建表逻辑
│   ├── models/                 # 数据模型（Product/Warehouse/Inventory/StockMovement）
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── warehouse.py
│   │   ├── inventory.py
│   │   └── stock_movement.py
│   └── routers/                # API 路由
│       ├── __init__.py
│       ├── products.py
│       ├── warehouses.py
│       ├── inventory.py
│       ├── inbound.py
│       ├── outbound.py
│       └── stock_movements.py
├── docs/
└── frontend/
```

## 4. 本地运行步骤

以下步骤基于 macOS / Linux 终端（Windows 可使用等价命令）：

1. 进入项目目录

```bash
cd /path/to/fresh-warehouse-demo
```

2. 创建虚拟环境

```bash
python3 -m venv .venv
```

3. 激活虚拟环境

```bash
source .venv/bin/activate
```

4. 安装依赖

```bash
pip install --upgrade pip
pip install fastapi uvicorn sqlmodel
```

5. 启动后端服务

```bash
cd backend
uvicorn main:app --reload
```

默认启动地址为：

- `http://127.0.0.1:8000`

## 5. API 文档（Swagger）

服务启动后，访问以下地址查看交互式 API 文档：

- Swagger UI：`http://127.0.0.1:8000/docs`

## 6. 版本说明

当前版本为原型 / MVP Demo，仅覆盖仓储核心流程的最小可用能力，用于演示与验证。  
它不是最终商业化系统，后续仍需补充权限、审计、异常处理、测试、部署与性能优化等企业级能力。

