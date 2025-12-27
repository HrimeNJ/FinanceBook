"""
Database Management Module

This module provides the DatabaseManager class for handling all database operations
including table creation, record management, and data querying for the Finance Book application.
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from models.category import Category
from models.record import Record
from models.user import User

def adapt_datetime(dt):
    return dt.isoformat()

def convert_datetime(s):
    return datetime.fromisoformat(s.decode())

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)

class DatabaseManager:
    """
    Database Manager Class

    Handles all database operations including initialization, CRUD operations,
    and data retrieval for users, categories, and financial records.
    """

    def __init__(self, db_path: str = "finance_book.db"):
        """
        初始化数据库管理器

        Args:
            db_path (str): 数据库文件路径
        """
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 用户表
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """
            )

            # 分类表 - 修改字段名以匹配Category类
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    parent_id INTEGER,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (parent_id) REFERENCES categories (category_id)
                )
            """
            )

            # 记录表 - 修改type字段为record_type以匹配Record类
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
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
                )
            """
            )

            conn.commit()

        # 使用Category类的静态方法初始化默认分类
        self._init_default_categories()

    def _init_default_categories(self):
        """使用Category类的静态方法初始化默认分类"""
        try:
            # 检查是否已经有分类数据
            existing_categories = self.query("SELECT COUNT(*) as count FROM categories")
            if existing_categories and existing_categories[0]["count"] > 0:
                return  # 如果已有分类数据，跳过初始化

            # 获取默认分类
            default_categories = Category.get_default_categories()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 先插入顶级分类（parent_id为None的）
                for cat_data in default_categories:
                    if cat_data.get("parent_id") is None:
                        cursor.execute(
                            "INSERT INTO categories (name, parent_id, is_active) VALUES (?, ?, ?)",
                            (cat_data["name"], None, True),
                        )

                # 再插入子分类
                for cat_data in default_categories:
                    if cat_data.get("parent_id") is not None:
                        cursor.execute(
                            "INSERT INTO categories (name, parent_id, is_active) VALUES (?, ?, ?)",
                            (cat_data["name"], cat_data["parent_id"], True),
                        )

                conn.commit()
                print("默认分类初始化完成")

        except Exception as e:
            print(f"初始化默认分类失败: {e}")

    def query(self, sql: str, params: tuple = ()) -> List[Dict]:
        """
        执行查询

        Args:
            sql (str): SQL查询语句
            params (tuple): 查询参数

        Returns:
            List[Dict]: 查询结果列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error executing query: {e}")
            return []

    # ==================== 用户相关方法 ====================

    def save_user(self, user: User) -> bool:
        """
        保存用户

        Args:
            user (User): 用户对象

        Returns:
            bool: 保存成功返回True，失败返回False
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                    (user.username, user.password_hash, user.email),
                )
                user.user_id = cursor.lastrowid
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error saving user: {e}")
            return False

    def get_user(
        self, user_id: Optional[int] = None, username: Optional[str] = None
    ) -> Optional[User]:
        """
        获取用户

        Args:
            user_id (Optional[int]): 用户ID
            username (Optional[str]): 用户名

        Returns:
            Optional[User]: 用户对象，未找到返回None
        """
        if user_id:
            result = self.query("SELECT * FROM users WHERE user_id = ?", (user_id,))
        elif username:
            result = self.query("SELECT * FROM users WHERE username = ?", (username,))
        else:
            return None

        return User.from_dict(result[0]) if result else None

    def update_user_login(self, user_id: int) -> bool:
        """
        更新用户最后登录时间

        Args:
            user_id (int): 用户ID

        Returns:
            bool: 更新成功返回True，失败返回False
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET last_login = ? WHERE user_id = ?",
                    (datetime.now(), user_id),
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error updating user login: {e}")
            return False

    # ==================== 分类相关方法 ====================

    def save_category(self, category: Category) -> bool:
        """
        保存分类

        Args:
            category (Category): 分类对象

        Returns:
            bool: 保存成功返回True，失败返回False
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if category.category_id is None or category.category_id == 0:
                    # 插入新分类
                    cursor.execute(
                        "INSERT INTO categories (name, parent_id, is_active) VALUES (?, ?, ?)",
                        (category.name, category.parent_id, category.is_active),
                    )
                    category.category_id = cursor.lastrowid
                else:
                    # 更新现有分类
                    cursor.execute(
                        "UPDATE categories SET name = ?, parent_id = ?, is_active = ? WHERE category_id = ?",
                        (
                            category.name,
                            category.parent_id,
                            category.is_active,
                            category.category_id,
                        ),
                    )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error saving category: {e}")
            return False

    def get_categories(self, active_only: bool = True) -> List[Category]:
        """
        获取分类列表

        Args:
            active_only (bool): 是否只获取活跃分类

        Returns:
            List[Category]: 分类对象列表
        """
        sql = "SELECT * FROM categories"
        if active_only:
            sql += " WHERE is_active = 1"
        sql += " ORDER BY name"

        results = self.query(sql)
        return [Category.from_dict(row) for row in results]

    def get_category(self, category_id: int) -> Optional[Category]:
        """
        获取单个分类

        Args:
            category_id (int): 分类ID

        Returns:
            Optional[Category]: 分类对象，未找到返回None
        """
        result = self.query(
            "SELECT * FROM categories WHERE category_id = ?", (category_id,)
        )
        return Category.from_dict(result[0]) if result else None

    # ==================== 记录相关方法 ====================

    def save_record(self, record: Record) -> bool:
        """
        保存记录

        Args:
            record (Record): 记录对象

        Returns:
            bool: 保存成功返回True，失败返回False
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if record.record_id is None or record.record_id == 0:
                    # 插入新记录
                    cursor.execute(
                        """
                        INSERT INTO records (amount, date, record_type, note, category_id, user_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            record.amount,
                            record.date,
                            record.record_type,
                            record.note,
                            record.category_id,
                            record.user_id,
                        ),
                    )
                    record.record_id = cursor.lastrowid
                else:
                    # 更新现有记录
                    cursor.execute(
                        """
                        UPDATE records 
                        SET amount=?, date=?, record_type=?, note=?, category_id=?, updated_at=?
                        WHERE record_id=?
                    """,
                        (
                            record.amount,
                            record.date,
                            record.record_type,
                            record.note,
                            record.category_id,
                            datetime.now(),
                            record.record_id,
                        ),
                    )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error saving record: {e}")
            return False

    def update_record(self, record: Record) -> bool:
        """
        更新记录（与save_record合并，保持兼容性）
        """
        return self.save_record(record)

    def delete_record(self, record_id: int) -> bool:
        """
        删除记录

        Args:
            record_id (int): 记录ID

        Returns:
            bool: 删除成功返回True，失败返回False
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM records WHERE record_id=?", (record_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error deleting record: {e}")
            return False

    def get_records(
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None,
        order_by: str = "date DESC",
        sort_column: Optional[str] = None,  # 新增危险参数
    ) -> List[Record]:
        """
        获取记录列表

        Args:
            user_id (int): 用户ID
            start_date (Optional[str]): 开始日期（YYYY-MM-DD格式）
            end_date (Optional[str]): 结束日期（YYYY-MM-DD格式）
            limit (Optional[int]): 限制返回数量
            order_by (str): 排序方式，默认按日期倒序

        Returns:
            List[Record]: 记录对象列表
        """
        # 验证 order_by 参数，防止 SQL 注入
        ALLOWED_ORDER_COLUMNS = ['date', 'amount', 'record_type', 'created_at', 'updated_at']
        ALLOWED_ORDER_DIRECTIONS = ['ASC', 'DESC']

        # 解析 order_by 参数
        order_parts = order_by.split()
        if len(order_parts) == 2:
            column, direction = order_parts
        elif len(order_parts) == 1:
            column = order_parts[0]
            direction = 'DESC'
        else:
            column = 'date'
            direction = 'DESC'
        
        # 验证列名和排序方向
        if column not in ALLOWED_ORDER_COLUMNS:
            column = 'date'
        if direction.upper() not in ALLOWED_ORDER_DIRECTIONS:
            direction = 'DESC'

        sql = "SELECT * FROM records WHERE user_id = ?"
        params = [user_id]

        if start_date and end_date:
            if len(start_date) == 10:  # 只有日期，没有时间
                start_date = f"{start_date} 00:00:00"
            if len(end_date) == 10:
                end_date = f"{end_date} 23:59:59"

            sql += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])

        sql += f" ORDER BY {column} {direction}"

        # 参数化 LIMIT 子句
        if limit is not None and isinstance(limit, int) and limit > 0:
            sql += " LIMIT ?"
            params.append(limit)

        results = self.query(sql, tuple(params))
        return [Record.from_dict(row) for row in results]

    def get_record(self, record_id: int) -> Optional[Record]:
        """
        获取单个记录

        Args:
            record_id (int): 记录ID

        Returns:
            Optional[Record]: 记录对象，未找到返回None
        """
        result = self.query("SELECT * FROM records WHERE record_id = ?", (record_id,))
        return Record.from_dict(result[0]) if result else None

    def get_all_records(self, user_id: int, limit: int = 10000) -> List[Record]:
        """
        加载所有记录
        
        Args:
            user_id (int): 用户ID
            limit (int): 最大返回数量,默认10000条(防止内存溢出)
        
        Returns:
            List[Record]: 记录列表
        """
        sql = "SELECT * FROM records WHERE user_id = ? ORDER BY date DESC LIMIT ?"
        
        results = self.query(sql, (user_id, limit))
        
        return [Record.from_dict(row) for row in results]

    # ==================== 统计方法 ====================

    def get_user_balance(self, user_id: int) -> Dict[str, float]:
        """
        获取用户余额统计

        Args:
            user_id (int): 用户ID

        Returns:
            Dict[str, float]: 包含总收入、总支出和余额的字典
        """
        income_result = self.query(
            "SELECT COALESCE(SUM(amount), 0) as total FROM records WHERE user_id = ? AND record_type = 'income'",
            (user_id,),
        )
        expense_result = self.query(
            "SELECT COALESCE(SUM(amount), 0) as total FROM records WHERE user_id = ? AND record_type = 'expense'",
            (user_id,),
        )

        total_income = float(income_result[0]["total"]) if income_result else 0.0
        total_expense = float(expense_result[0]["total"]) if expense_result else 0.0

        return {
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense,
        }

    def get_records_by_period(
        self, user_id: int, period: str = "month"
    ) -> List[Record]:
        """
        根据时间段获取记录

        Args:
            user_id (int): 用户ID
            period (str): 时间段 ('today', 'week', 'month', 'year')

        Returns:
            List[Record]: 记录列表
        """
        now = datetime.now()

        if period == "today":
            start_date = now.strftime("%Y-%m-%d")
            end_date = start_date
        elif period == "week":
            start_date = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
            end_date = now.strftime("%Y-%m-%d")
        elif period == "month":
            start_date = now.replace(day=1).strftime("%Y-%m-%d")
            end_date = now.strftime("%Y-%m-%d")
        elif period == "year":
            start_date = now.replace(month=1, day=1).strftime("%Y-%m-%d")
            end_date = now.strftime("%Y-%m-%d")
        else:
            return self.get_records(user_id)

        return self.get_records(user_id, start_date, end_date)
