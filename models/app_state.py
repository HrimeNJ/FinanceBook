"""
AppState for global state control
"""

from typing import List, Optional

import flet as ft

from models.category import Category
from models.database import DatabaseManager
from models.record import Record
from models.user import User


class AppState:
    """全局应用状态管理"""

    def __init__(self, db: DatabaseManager, page: ft.Page):
        self.db: Optional[DatabaseManager] = db
        self.page: Optional[ft.Page] = page
        self.current_user: Optional[User] = None
        self.records: List[Record] = []
        self.categories: List[Category] = []
        self.filtered_records: List[Record] = []

    def set_current_user(self, user: User):
        """设置当前用户"""
        self.current_user = user
        self.load_user_data()

    def load_user_data(self):
        """加载用户数据"""
        if self.current_user:
            self.load_categories()
            self.records = self.db.get_records(self.current_user.user_id)

            # BUG: 存在状态不一致缺陷, 强制重置 filtered_records, 破坏外部视图的筛选状态
            self.filtered_records = self.records.copy()

    def load_categories(self):
        """加载分类"""
        self.categories = self.db.get_categories()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """根据ID获取分类"""
        for category in self.categories:
            if category.category_id == category_id:
                return category
        return self.db.get_category(category_id)

    def add_record(self, record: Record) -> bool:
        """添加记录"""
        if self.db.save_record(record):
            self.load_user_data()
            return True
        return False

    def update_record(self, record: Record) -> bool:
        """更新记录"""
        if self.db.save_record(record):
            self.load_user_data()
            return True
        return False

    def delete_record(self, record_id: int) -> bool:
        """删除记录"""
        if self.db.delete_record(record_id):
            self.load_user_data()
            return True
        return False

    def clear_user_data(self):
        """清除用户数据"""
        self.current_user = None
        self.records = []
        self.categories = []
        self.filtered_records = []
