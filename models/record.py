"""
Record class in FinanceBook
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Record:
    record_id: Optional[int] = None
    amount: float = 0.0
    date: datetime = None
    record_type: str = ""  # 'income' or 'expense'
    note: str = ""
    category_id: int = 0
    user_id: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "record_id": self.record_id,
            "amount": self.amount,
            "date": self.date.isoformat() if self.date else None,
            "type": self.record_type,
            "note": self.note,
            "category_id": self.category_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Record":
        """从字典创建记录对象"""
        return cls(
            record_id=data.get("record_id"),
            amount=data.get("amount", 0.0),
            date=(
                datetime.fromisoformat(data["date"])
                if data.get("date")
                else datetime.now()
            ),
            record_type=data.get("record_type", ""),
            note=data.get("note", ""),
            category_id=data.get("category_id", 0),
            user_id=data.get("user_id", 0),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
            updated_at=(
                datetime.fromisoformat(data["updated_at"])
                if data.get("updated_at")
                else None
            ),
        )
