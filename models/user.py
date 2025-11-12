"""
User class in FinanceBook
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    user_id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    email: str = ""
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """从字典创建用户对象"""
        return cls(
            user_id=data.get("user_id"),
            username=data.get("username", ""),
            password_hash=data.get("password_hash", ""),
            email=data.get("email", ""),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
            last_login=(
                datetime.fromisoformat(data["last_login"])
                if data.get("last_login")
                else None
            ),
        )
