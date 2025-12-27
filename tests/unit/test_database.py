# tests/unit/test_database.py
"""
DatabaseManager 单元测试
目标：达到 80% 以上的代码覆盖率
"""

import os
import sqlite3
import tempfile
from datetime import datetime

import pytest

from models.category import Category
from models.database import DatabaseManager
from models.record import Record
from models.user import User


@pytest.fixture
def temp_db():
    """创建临时数据库用于测试"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as f:
        db_path = f.name
    
    yield db_path
    
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def db_manager(temp_db):
    """创建 DatabaseManager 实例"""
    return DatabaseManager(temp_db)


@pytest.fixture
def sample_user():
    """创建样例用户"""
    return User(
        username="testuser",
        password_hash="hashed_password_123",
        email="test@example.com"
    )


@pytest.fixture
def sample_category():
    """创建样例分类"""
    return Category(
        name="Food",
        parent_id=None,
        is_active=True
    )


class TestDatabaseInitialization:
    """测试数据库初始化"""
    
    def test_database_initialization(self, db_manager, temp_db):
        """测试1：数据库初始化（表创建+默认分类）"""
        # 验证文件存在
        assert os.path.exists(temp_db)
        
        # 验证表创建
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        assert 'users' in tables
        assert 'categories' in tables
        assert 'records' in tables
        
        # 验证默认分类
        categories = db_manager.get_categories()
        assert len(categories) > 0
        category_names = [c.name for c in categories]
        assert "Food & Dining" in category_names


class TestUserOperations:
    """测试用户相关操作"""
    
    def test_user_crud_operations(self, db_manager, sample_user):
        """测试2：用户CRUD操作（保存、获取、更新）"""
        # 保存用户
        assert db_manager.save_user(sample_user)
        assert sample_user.user_id is not None
        
        # 通过ID获取
        retrieved_user = db_manager.get_user(user_id=sample_user.user_id)
        assert retrieved_user.username == "testuser"
        
        # 通过用户名获取
        retrieved_user = db_manager.get_user(username="testuser")
        assert retrieved_user.user_id == sample_user.user_id
        
        # 更新登录时间
        assert db_manager.update_user_login(sample_user.user_id)
        updated_user = db_manager.get_user(user_id=sample_user.user_id)
        assert updated_user.last_login is not None
    
    def test_duplicate_username_fails(self, db_manager, sample_user):
        """测试3：重复用户名失败"""
        db_manager.save_user(sample_user)
        
        duplicate = User(
            username="testuser",
            password_hash="different",
            email="different@example.com"
        )
        assert db_manager.save_user(duplicate) is False
    
    def test_nonexistent_user(self, db_manager):
        """测试4：不存在的用户返回None"""
        assert db_manager.get_user(user_id=999) is None
        # 测试无参数调用 get_user (覆盖第212行)
        assert db_manager.get_user() is None


class TestCategoryOperations:
    """测试分类相关操作"""
    
    def test_category_operations(self, db_manager, sample_category):
        """测试5：分类操作（保存、获取）"""
        # 保存新分类
        assert db_manager.save_category(sample_category)
        assert sample_category.category_id is not None
        
        # 更新现有分类 (覆盖第263行及274-276行)
        sample_category.name = "Updated Food"
        sample_category.is_active = False
        assert db_manager.save_category(sample_category)
        
        # 获取活跃分类
        categories = db_manager.get_categories(active_only=True)
        for cat in categories:
            assert cat.is_active in (True, 1)
        
        # 获取所有分类（包括非活跃）
        all_categories = db_manager.get_categories(active_only=False)
        assert len(all_categories) >= len(categories)
        
        # 通过ID获取
        retrieved_cat = db_manager.get_category(sample_category.category_id)
        assert retrieved_cat.name == "Updated Food"


class TestRecordOperations:
    """测试记录相关操作"""
    
    def test_record_crud_operations(self, db_manager, sample_user, sample_category):
        """测试6：记录CRUD操作（保存、获取、更新、删除）"""
        db_manager.save_user(sample_user)
        db_manager.save_category(sample_category)
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 创建记录
        record = Record(
            amount=100.50,
            date=f"{today} 12:00:00",
            record_type="expense",
            note="Test expense",
            category_id=sample_category.category_id,
            user_id=sample_user.user_id
        )
        
        # 保存新记录
        assert db_manager.save_record(record)
        assert record.record_id is not None
        
        # 获取
        records = db_manager.get_records(user_id=sample_user.user_id)
        assert len(records) == 1
        assert records[0].amount == 100.50
        
        # 更新现有记录 (覆盖第363-365行)
        record.amount = 200.00
        record.note = "Updated"
        assert db_manager.update_record(record)
        updated = db_manager.get_record(record.record_id)
        assert updated.amount == 200.00
        
        # 删除
        assert db_manager.delete_record(record.record_id)
        assert db_manager.get_record(record.record_id) is None
    
    def test_get_records_with_filters(self, db_manager, sample_user, sample_category):
        """测试7：记录过滤（日期、数量限制）"""
        db_manager.save_user(sample_user)
        db_manager.save_category(sample_category)
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 创建多条记录
        for i in range(5):
            record = Record(
                amount=100.0 + i,
                date=f"{today} 12:00:00",
                record_type="expense",
                note=f"Record {i}",
                category_id=sample_category.category_id,
                user_id=sample_user.user_id
            )
            db_manager.save_record(record)
        
        # 日期过滤（覆盖第426和432行的时间格式处理）
        records = db_manager.get_records(
            user_id=sample_user.user_id,
            start_date=today,  # 只有日期，触发时间补全逻辑
            end_date=today
        )
        assert len(records) == 5
        
        # 数量限制
        records = db_manager.get_records(user_id=sample_user.user_id, limit=3)
        assert len(records) == 3
    
    def test_get_all_records(self, db_manager, sample_user, sample_category):
        """测试8：获取所有记录"""
        db_manager.save_user(sample_user)
        db_manager.save_category(sample_category)
        
        today = datetime.now().strftime("%Y-%m-%d")
        record = Record(
            amount=50.0,
            date=f"{today} 12:00:00",
            record_type="income",
            note="Test",
            category_id=sample_category.category_id,
            user_id=sample_user.user_id
        )
        db_manager.save_record(record)
        
        records = db_manager.get_all_records(user_id=sample_user.user_id)
        assert len(records) >= 1


class TestStatisticalMethods:
    """测试统计方法"""
    
    def test_user_balance(self, db_manager, sample_user, sample_category):
        """测试9：用户余额统计"""
        db_manager.save_user(sample_user)
        db_manager.save_category(sample_category)
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 支出
        expense = Record(
            amount=100.50,
            date=f"{today} 12:00:00",
            record_type="expense",
            note="Expense",
            category_id=sample_category.category_id,
            user_id=sample_user.user_id
        )
        db_manager.save_record(expense)
        
        # 收入
        income = Record(
            amount=500.0,
            date=f"{today} 12:00:00",
            record_type="income",
            note="Income",
            category_id=sample_category.category_id,
            user_id=sample_user.user_id
        )
        db_manager.save_record(income)
        
        balance = db_manager.get_user_balance(user_id=sample_user.user_id)
        assert balance['income'] == 500.0
        assert balance['expense'] == 100.50
        assert balance['balance'] == 399.50
    
    def test_records_by_period(self, db_manager, sample_user, sample_category):
        """测试10：按时间段获取记录（today/week/month/year）"""
        db_manager.save_user(sample_user)
        db_manager.save_category(sample_category)
        
        today = datetime.now().strftime("%Y-%m-%d")
        record = Record(
            amount=100.0,
            date=f"{today} 12:00:00",
            record_type="expense",
            note="Test",
            category_id=sample_category.category_id,
            user_id=sample_user.user_id
        )
        db_manager.save_record(record)
        
        # 测试各个时间段 (覆盖第507-517行)
        for period in ['today', 'week', 'month', 'year']:
            records = db_manager.get_records_by_period(
                user_id=sample_user.user_id,
                period=period
            )
            assert len(records) >= 1, f"Period {period} failed"
        
        # 测试无效的 period 参数 (覆盖第517行的 else 分支)
        records = db_manager.get_records_by_period(
            user_id=sample_user.user_id,
            period="invalid_period"
        )
        assert isinstance(records, list)


class TestQueryMethod:
    """测试通用查询方法"""
    
    def test_query_method(self, db_manager, sample_user):
        """测试11：通用查询方法"""
        db_manager.save_user(sample_user)
        
        # 带参数查询
        results = db_manager.query(
            "SELECT * FROM users WHERE username = ?",
            ("testuser",)
        )
        assert isinstance(results, list)
        assert len(results) > 0
        assert isinstance(results[0], dict)
        assert results[0]['username'] == "testuser"
        
        # 无参数查询
        results = db_manager.query("SELECT * FROM categories")
        assert isinstance(results, list)


class TestEdgeCases:
    """测试边界情况和安全性"""
    
    def test_empty_database(self, temp_db):
        """测试12：空数据库查询"""
        db = DatabaseManager(temp_db)
        users = db.query("SELECT * FROM users")
        assert users == []
    
    def test_invalid_operations(self, db_manager):
        """测试13：无效操作"""
        # 删除不存在的记录 (覆盖第389-391行)
        assert db_manager.delete_record(99999) is False
        
        # 获取不存在的分类
        assert db_manager.get_category(99999) is None
    
    def test_sql_injection_protection(self, db_manager, sample_user):
        """测试14：SQL注入防护"""
        db_manager.save_user(sample_user)
        
        # 尝试SQL注入
        malicious = "testuser' OR '1'='1"
        user = db_manager.get_user(username=malicious)
        assert user is None
    
    def test_connection_handling(self, db_manager):
        """测试15：连接资源管理"""
        # 执行多次查询，检测连接泄漏
        for _ in range(100):
            db_manager.query("SELECT 1")
        assert True  # 如果没有异常，测试通过
    
    def test_records_with_complete_timestamp(self, db_manager, sample_user, sample_category):
        """测试16：完整时间戳格式的日期查询"""
        db_manager.save_user(sample_user)
        db_manager.save_category(sample_category)
        
        today = datetime.now().strftime("%Y-%m-%d")
        record = Record(
            amount=75.0,
            date=f"{today} 15:30:45",
            record_type="income",
            note="With timestamp",
            category_id=sample_category.category_id,
            user_id=sample_user.user_id
        )
        db_manager.save_record(record)
        
        records = db_manager.get_records(
            user_id=sample_user.user_id,
            start_date=f"{today} 00:00:00",
            end_date=f"{today} 23:59:59"
        )
        assert len(records) >= 1