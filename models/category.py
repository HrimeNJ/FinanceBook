"""
Category class in FinanceBook
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Category:
    category_id: Optional[int] = None
    name: str = ""
    parent_id: Optional[int] = None
    is_active: bool = True

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "category_id": self.category_id,
            "name": self.name,
            "parent_id": self.parent_id,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """从字典创建分类对象"""
        return cls(
            category_id=data.get("category_id"),
            name=data.get("name", ""),
            parent_id=data.get("parent_id"),
            is_active=data.get("is_active", True),
        )

    @staticmethod
    def get_default_categories() -> List[dict]:
        """Get default categories"""
        return [
            {"name": "Food & Dining", "parent_id": None},
            {"name": "Breakfast", "parent_id": 1},
            {"name": "Lunch", "parent_id": 1},
            {"name": "Dinner", "parent_id": 1},
            {"name": "Transportation", "parent_id": None},
            {"name": "Bus", "parent_id": 5},
            {"name": "Subway", "parent_id": 5},
            {"name": "Taxi", "parent_id": 5},
            {"name": "Entertainment", "parent_id": None},
            {"name": "Movies", "parent_id": 9},
            {"name": "Games", "parent_id": 9},
            {"name": "Salary", "parent_id": None},
            {"name": "Investment Returns", "parent_id": None},
            {"name": "Daily Necessities", "parent_id": None},
            {"name": "Healthcare", "parent_id": None},
            {"name": "Shopping", "parent_id": None},
            {"name": "Utilities", "parent_id": None},
            {"name": "Education", "parent_id": None},
            {"name": "Travel", "parent_id": None},
            {"name": "Gift & Donation", "parent_id": None},
        ]
