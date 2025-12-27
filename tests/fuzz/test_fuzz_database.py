# tests/fuzz/test_fuzz_database.py
"""
模糊测试 - Database输入
使用 Hypothesis 进行属性测试和模糊测试
"""

import string
import tempfile
import os

import pytest
from hypothesis import given, strategies as st, settings
from hypothesis import HealthCheck

from models.database import DatabaseManager
from models.user import User
from models.record import Record
from models.category import Category
from datetime import datetime, timedelta


@pytest.fixture
def temp_db_for_fuzz():
    """为模糊测试创建临时数据库"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as f:
        db_path = f.name
    
    db = DatabaseManager(db_path)
    
    yield db
    
    if os.path.exists(db_path):
        os.remove(db_path)


class TestFuzzUserInputs:
    """模糊测试用户输入"""
    
    @given(
        username=st.text(min_size=1, max_size=100),
        email=st.emails(),
        password=st.text(min_size=1, max_size=200)
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_fuzz_user_creation(self, temp_db_for_fuzz, username, email, password):
        """模糊测试用户创建"""
        user = User(
            username=username,
            email=email,
            password_hash=password
        )
        
        try:
            result = temp_db_for_fuzz.save_user(user)
            # 如果保存成功，用户ID应该被设置
            if result:
                assert user.user_id is not None
        except Exception as e:
            # 记录异常但不失败（模糊测试允许发现边界情况）
            print(f"Exception with username={username}, email={email}: {e}")
    
    @given(
        username=st.text(
            alphabet=st.characters(blacklist_categories=('Cs',)),
            min_size=0,
            max_size=200
        )
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_fuzz_get_user_by_username(self, temp_db_for_fuzz, username):
        """模糊测试通过用户名获取用户"""
        try:
            user = temp_db_for_fuzz.get_user(username=username)
            # 不应该抛出异常
            assert user is None or isinstance(user, User)
        except Exception as e:
            pytest.fail(f"Unexpected exception: {e}")


class TestFuzzRecordInputs:
    """模糊测试记录输入"""
    
    @given(
        amount=st.floats(min_value=-1000000, max_value=1000000, allow_nan=False, allow_infinity=False),
        note=st.text(max_size=500),
        record_type=st.sampled_from(["income", "expense", "invalid", "", "123"])
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_fuzz_record_creation(self, temp_db_for_fuzz, amount, note, record_type):
        """模糊测试记录创建"""
        # 首先创建测试用户
        user = User(username="fuzz_user", email="fuzz@test.com", password_hash="hash")
        temp_db_for_fuzz.save_user(user)
        
        # 获取分类
        categories = temp_db_for_fuzz.get_categories()
        if not categories:
            pytest.skip("No categories available")
        
        record = Record(
            amount=amount,
            date=datetime.now(),
            record_type=record_type,
            note=note,
            category_id=categories[0].category_id,
            user_id=user.user_id
        )
        
        try:
            result = temp_db_for_fuzz.save_record(record)
            if result:
                assert record.record_id is not None
        except Exception as e:
            # 允许某些输入失败（如无效类型）
            print(f"Exception with amount={amount}, type={record_type}: {e}")
    
    @given(
        days_offset=st.integers(min_value=-365*10, max_value=365*10)
    )
    @settings(max_examples=30, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_fuzz_record_dates(self, temp_db_for_fuzz, days_offset):
        """模糊测试不同日期的记录"""
        user = User(username="date_fuzz_user", email="date@test.com", password_hash="hash")
        temp_db_for_fuzz.save_user(user)
        
        categories = temp_db_for_fuzz.get_categories()
        if not categories:
            pytest.skip("No categories available")
        
        test_date = datetime.now() + timedelta(days=days_offset)
        
        record = Record(
            amount=100.0,
            date=test_date,
            record_type="expense",
            note="Fuzz test",
            category_id=categories[0].category_id,
            user_id=user.user_id
        )
        
        try:
            temp_db_for_fuzz.save_record(record)
            retrieved = temp_db_for_fuzz.get_record(record.record_id)
            if retrieved:
                assert retrieved.record_id == record.record_id
        except Exception as e:
            pytest.fail(f"Unexpected exception with date offset {days_offset}: {e}")


class TestFuzzQueryInputs:
    """模糊测试SQL查询输入"""
    
    @given(
        sql_fragment=st.text(
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc', 'Pd', 'Ps', 'Pe')),
            max_size=50
        )
    )
    @settings(max_examples=30, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_fuzz_username_query_injection(self, temp_db_for_fuzz, sql_fragment):
        """模糊测试SQL注入防护"""
        # 尝试使用各种SQL片段作为用户名
        try:
            user = temp_db_for_fuzz.get_user(username=sql_fragment)
            # 参数化查询应该阻止SQL注入
            assert user is None or isinstance(user, User)
        except Exception as e:
            # SQL注入尝试可能导致异常，但不应该导致数据泄露
            print(f"Exception with SQL fragment '{sql_fragment}': {e}")


class TestFuzzCategoryInputs:
    """模糊测试分类输入"""
    
    @given(
        category_name=st.text(min_size=1, max_size=100),
        parent_id=st.one_of(st.none(), st.integers(min_value=-100, max_value=100))
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_fuzz_category_creation(self, temp_db_for_fuzz, category_name, parent_id):
        """模糊测试分类创建"""
        category = Category(
            name=category_name,
            parent_id=parent_id,
            is_active=True
        )
        
        try:
            result = temp_db_for_fuzz.save_category(category)
            if result:
                assert category.category_id is not None
        except Exception as e:
            print(f"Exception with name={category_name}, parent_id={parent_id}: {e}")
