# tests/integration/test_user_workflow.py
"""
集成测试 - 用户工作流
测试用户从注册到记账的完整流程
"""

import os
import tempfile

import pytest

from models.app_state import AppState
from models.database import DatabaseManager
from models.record import Record
from models.user import User
from models.category import Category
from datetime import datetime, timedelta


@pytest.fixture
def integrated_system():
    """创建完整的集成测试环境"""
    # 创建临时数据库
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as f:
        db_path = f.name
    
    # 初始化系统组件
    db_manager = DatabaseManager(db_path)
    
    # 创建mock page对象
    from unittest.mock import Mock
    mock_page = Mock()
    
    app_state = AppState(db_manager, mock_page)
    
    yield {
        'db': db_manager,
        'state': app_state,
        'db_path': db_path
    }
    
    # 清理
    if os.path.exists(db_path):
        os.remove(db_path)


class TestUserRegistrationToRecording:
    """集成测试1：用户注册到记账的完整流程"""
    
    def test_complete_user_workflow(self, integrated_system):
        """完整的用户工作流测试"""
        db = integrated_system['db']
        state = integrated_system['state']
        
        # 步骤1：用户注册
        new_user = User(
            username="integration_user",
            password_hash="hashed_password",
            email="integration@test.com"
        )
        
        assert db.save_user(new_user)
        assert new_user.user_id is not None
        
        # 步骤2：用户登录（设置当前用户）
        state.set_current_user(new_user)
        assert state.current_user == new_user
        
        # 步骤3：验证分类已加载
        assert len(state.categories) > 0
        first_category = state.categories[0]
        
        # 步骤4：添加支出记录
        expense = Record(
            amount=50.00,
            date=datetime.now(),
            record_type="expense",
            note="Integration test expense",
            category_id=first_category.category_id,
            user_id=new_user.user_id
        )
        
        assert state.add_record(expense)
        assert expense.record_id is not None
        
        # 步骤5：验证记录已保存
        assert len(state.records) == 1
        assert state.records[0].amount == 50.00
        
        # 步骤6：添加收入记录
        income = Record(
            amount=1000.00,
            date=datetime.now(),
            record_type="income",
            note="Integration test income",
            category_id=first_category.category_id,
            user_id=new_user.user_id
        )
        
        assert state.add_record(income)
        
        # 步骤7：验证多条记录
        assert len(state.records) == 2
        
        # 步骤8：更新记录
        expense.amount = 75.00
        expense.note = "Updated expense"
        assert state.update_record(expense)
        
        # 步骤9：验证更新
        updated_record = db.get_record(expense.record_id)
        assert updated_record.amount == 75.00
        
        # 步骤10：删除记录
        assert state.delete_record(income.record_id)
        assert len(state.records) == 1
        
        # 步骤11：验证最终状态
        final_records = db.get_records(new_user.user_id)
        assert len(final_records) == 1
        assert final_records[0].record_id == expense.record_id


class TestMultiUserScenario:
    """集成测试2：多用户场景"""
    
    def test_multiple_users_independent_data(self, integrated_system):
        """测试多用户数据隔离"""
        db = integrated_system['db']
        state = integrated_system['state']
        
        # 创建用户1
        user1 = User(
            username="user1",
            password_hash="hash1",
            email="user1@test.com"
        )
        db.save_user(user1)
        
        # 创建用户2
        user2 = User(
            username="user2",
            password_hash="hash2",
            email="user2@test.com"
        )
        db.save_user(user2)
        
        # 获取分类
        categories = db.get_categories()
        category_id = categories[0].category_id
        
        # 用户1添加记录
        state.set_current_user(user1)
        record1 = Record(
            amount=100.00,
            date=datetime.now(),
            record_type="expense",
            note="User1's expense",
            category_id=category_id,
            user_id=user1.user_id
        )
        state.add_record(record1)
        
        # 用户2添加记录
        state.set_current_user(user2)
        record2 = Record(
            amount=200.00,
            date=datetime.now(),
            record_type="expense",
            note="User2's expense",
            category_id=category_id,
            user_id=user2.user_id
        )
        state.add_record(record2)
        
        # 验证数据隔离
        user1_records = db.get_records(user1.user_id)
        user2_records = db.get_records(user2.user_id)
        
        assert len(user1_records) == 1
        assert len(user2_records) == 1
        assert user1_records[0].amount == 100.00
        assert user2_records[0].amount == 200.00
        assert user1_records[0].note == "User1's expense"
        assert user2_records[0].note == "User2's expense"


class TestCategoryManagement:
    """集成测试3：分类管理流程"""
    
    def test_category_crud_workflow(self, integrated_system):
        """测试分类的创建、使用和管理"""
        db = integrated_system['db']
        state = integrated_system['state']
        
        # 创建用户
        user = User(
            username="category_user",
            password_hash="hash",
            email="category@test.com"
        )
        db.save_user(user)
        state.set_current_user(user)
        
        # 创建自定义分类
        custom_category = Category(
            name="Custom Shopping",
            parent_id=None,
            is_active=True
        )
        assert db.save_category(custom_category)
        assert custom_category.category_id is not None
        
        # 重新加载分类到state
        state.load_categories()
        
        # 使用自定义分类创建记录
        record = Record(
            amount=150.00,
            date=datetime.now(),
            record_type="expense",
            note="Shopping with custom category",
            category_id=custom_category.category_id,
            user_id=user.user_id
        )
        assert state.add_record(record)
        
        # 验证分类被正确使用
        retrieved_category = state.get_category_by_id(custom_category.category_id)
        assert retrieved_category is not None
        assert retrieved_category.name == "Custom Shopping"


class TestBalanceCalculation:
    """集成测试4：余额计算和统计"""
    
    def test_balance_tracking(self, integrated_system):
        """测试收支平衡计算"""
        db = integrated_system['db']
        state = integrated_system['state']
        
        # 创建用户
        user = User(
            username="balance_user",
            password_hash="hash",
            email="balance@test.com"
        )
        db.save_user(user)
        state.set_current_user(user)
        
        category_id = state.categories[0].category_id
        
        # 添加多笔收入
        incomes = [500.00, 1000.00, 300.00]
        for amount in incomes:
            income = Record(
                amount=amount,
                date=datetime.now(),
                record_type="income",
                note="Income",
                category_id=category_id,
                user_id=user.user_id
            )
            state.add_record(income)
        
        # 添加多笔支出
        expenses = [200.00, 150.00, 50.00]
        for amount in expenses:
            expense = Record(
                amount=amount,
                date=datetime.now(),
                record_type="expense",
                note="Expense",
                category_id=category_id,
                user_id=user.user_id
            )
            state.add_record(expense)
        
        # 计算余额
        balance = db.get_user_balance(user.user_id)
        
        total_income = sum(incomes)
        total_expense = sum(expenses)
        expected_balance = total_income - total_expense
        
        assert balance['income'] == total_income
        assert balance['expense'] == total_expense
        assert balance['balance'] == expected_balance


class TestRecordFiltering:
    """集成测试5：记录过滤和查询"""
    
    def test_date_range_filtering(self, integrated_system):
        """测试按日期范围过滤记录"""
        db = integrated_system['db']
        state = integrated_system['state']
        
        # 创建用户
        user = User(
            username="filter_user",
            password_hash="hash",
            email="filter@test.com"
        )
        db.save_user(user)
        state.set_current_user(user)
        
        category_id = state.categories[0].category_id
        today = datetime.now()
        
        # 创建不同日期的记录 - 使用字符串格式
        dates = [
            (today - timedelta(days=7)).strftime("%Y-%m-%d 12:00:00"),  # 一周前
            (today - timedelta(days=3)).strftime("%Y-%m-%d 12:00:00"),  # 三天前
            today.strftime("%Y-%m-%d 12:00:00"),                        # 今天
        ]
        
        for i, date in enumerate(dates):
            record = Record(
                amount=100.00 * (i + 1),
                date=date,
                record_type="expense",
                note=f"Record {i}",
                category_id=category_id,
                user_id=user.user_id
            )
            state.add_record(record)
        
        # 测试按周查询
        week_records = db.get_records_by_period(user.user_id, "week")
        assert len(week_records) >= 2  # 至少包含今天和三天前
        
        # 测试按今天查询
        today_records = db.get_records_by_period(user.user_id, "today")
        assert len(today_records) >= 1


class TestStateManagement:
    """集成测试6：状态管理和数据同步"""
    
    def test_state_data_synchronization(self, integrated_system):
        """测试AppState和数据库的数据同步"""
        db = integrated_system['db']
        state = integrated_system['state']
        
        # 创建用户
        user = User(
            username="sync_user",
            password_hash="hash",
            email="sync@test.com"
        )
        db.save_user(user)
        state.set_current_user(user)
        
        category_id = state.categories[0].category_id
        
        # 通过state添加记录
        record1 = Record(
            amount=100.00,
            date=datetime.now(),
            record_type="expense",
            note="State record",
            category_id=category_id,
            user_id=user.user_id
        )
        state.add_record(record1)
        
        # 验证state中的数据
        assert len(state.records) == 1
        
        # 直接通过数据库添加记录
        record2 = Record(
            amount=200.00,
            date=datetime.now(),
            record_type="income",
            note="DB record",
            category_id=category_id,
            user_id=user.user_id
        )
        db.save_record(record2)
        
        # 重新加载用户数据
        state.load_user_data()
        
        # 验证同步后的数据
        assert len(state.records) == 2
        
        # 测试删除后的同步
        state.delete_record(record1.record_id)
        assert len(state.records) == 1
        assert state.records[0].record_id == record2.record_id


class TestUserSessionManagement:
    """集成测试7：用户会话管理"""
    
    def test_user_login_logout_workflow(self, integrated_system):
        """测试用户登录登出流程"""
        db = integrated_system['db']
        state = integrated_system['state']
        
        # 创建两个用户
        user1 = User(
            username="session_user1",
            password_hash="hash1",
            email="session1@test.com"
        )
        user2 = User(
            username="session_user2",
            password_hash="hash2",
            email="session2@test.com"
        )
        db.save_user(user1)
        db.save_user(user2)
        
        category_id = db.get_categories()[0].category_id
        
        # 用户1登录并添加记录
        state.set_current_user(user1)
        record1 = Record(
            amount=100.00,
            date=datetime.now(),
            record_type="expense",
            note="User1 record",
            category_id=category_id,
            user_id=user1.user_id
        )
        state.add_record(record1)
        assert len(state.records) == 1
        
        # 切换到用户2
        state.clear_user_data()
        assert state.current_user is None
        assert len(state.records) == 0
        
        state.set_current_user(user2)
        record2 = Record(
            amount=200.00,
            date=datetime.now(),
            record_type="income",
            note="User2 record",
            category_id=category_id,
            user_id=user2.user_id
        )
        state.add_record(record2)
        
        # 验证用户2的数据
        assert len(state.records) == 1
        assert state.records[0].amount == 200.00
        
        # 切换回用户1
        state.set_current_user(user1)
        assert len(state.records) == 1
        assert state.records[0].amount == 100.00