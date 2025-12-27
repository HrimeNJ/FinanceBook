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

        try:
            amount = float(data.get("amount", 0.0))
        except (ValueError, TypeError):
            amount = 0.0
        
        try:
            date = datetime.fromisoformat(data["date"]) if data.get("date") else datetime.now()
        except (ValueError, TypeError, KeyError):
            date = datetime.now()
        
        record_type = data.get("record_type", "")
        if record_type not in ["income", "expense", ""]:
            record_type = ""
        
        try:
            record_id = int(data["record_id"]) if data.get("record_id") is not None else None
        except (ValueError, TypeError):
            record_id = None

        try:
            category_id = int(data.get("category_id", 0))
        except (ValueError, TypeError):
            category_id = 0
        
        try:
            user_id = int(data.get("user_id", 0))
        except (ValueError, TypeError):
            user_id = 0
        
        try:
            created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        except (ValueError, TypeError, KeyError):
            created_at = None
        
        try:
            updated_at = datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
        except (ValueError, TypeError, KeyError):
            updated_at = None

        note = str(data.get("note", "")) if data.get("note") is not None else ""
        
        return cls(
            record_id=record_id,
            amount=amount,
            date=date,
            record_type=record_type,
            note=note,
            category_id=category_id,
            user_id=user_id,
            created_at=created_at,
            updated_at=updated_at,
        )