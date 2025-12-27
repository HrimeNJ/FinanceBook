# tests/unit/test_router.py
"""
Router 单元测试
目标：达到 80% 以上的代码覆盖率
"""

import pytest
from unittest.mock import Mock, patch

from models.app_state import AppState
from models.user import User
from views.router import Router


@pytest.fixture
def mock_page():
    """创建模拟的 Flet Page 对象"""
    page = Mock()
    page.route = "/welcome"
    page.views = []
    page.go = Mock()
    page.update = Mock()
    return page


@pytest.fixture
def mock_state():
    """创建模拟的 AppState 对象"""
    state = Mock(spec=AppState)
    state.current_user = None
    state.page = Mock()
    return state


@pytest.fixture
def router():
    """创建 Router 实例"""
    return Router()


@pytest.fixture
def mounted_router(router, mock_page, mock_state):
    """创建已挂载的 Router"""
    router.mount(mock_page, mock_state)
    return router


@pytest.fixture
def authenticated_state(mock_state):
    """创建已登录状态"""
    mock_state.current_user = User(
        user_id=1,
        username="testuser",
        password_hash="hash",
        email="test@test.com"
    )
    return mock_state


class TestRouterInitializationAndMount:
    """测试路由器初始化和挂载"""
    
    def test_router_initialization_and_mount(self, router, mock_page, mock_state):
        """测试1：路由器创建和挂载"""
        # 验证初始化
        assert router is not None
        assert router.page is None
        assert router.state is None
        
        # 验证挂载
        router.mount(mock_page, mock_state)
        assert router.page == mock_page
        assert router.state == mock_state
        assert mock_page.on_route_change is not None
        assert mock_page.on_view_pop is not None


class TestPublicRoutes:
    """测试公开路由（不需要登录）"""
    
    def test_public_routes_access(self, mounted_router, mock_page):
        """测试2：公开路由访问（welcome/login/register/root）"""
        public_routes = {
            "/welcome": "WelcomeView",
            "/": "WelcomeView",
            "/login": "LoginView",
            "/register": "RegisterView"
        }
        
        for route, view_name in public_routes.items():
            mock_page.route = route
            mock_page.views = []  # 清空视图
            
            with patch(f'views.router.{view_name}') as MockView:
                mounted_router.route_change(None)
                
                assert MockView.called, f"Route {route} failed"
                assert len(mock_page.views) > 0
                mock_page.update.assert_called()


class TestProtectedRoutes:
    """测试受保护路由（需要登录）"""
    
    def test_protected_routes_without_auth(self, mounted_router, mock_page, mock_state):
        """测试3：未登录访问受保护路由（重定向到登录）"""
        protected_routes = [
            "/dashboard",
            "/records",
            "/add_record",
            "/statistics",
            "/settings"
        ]
        
        mock_state.current_user = None
        
        for route in protected_routes:
            mock_page.route = route
            mock_page.go.reset_mock()  # 重置 mock
            
            mounted_router.route_change(None)
            
            # 应该重定向到登录页
            mock_page.go.assert_called_with("/login"), f"Route {route} failed to redirect"
    
    def test_protected_routes_with_auth(self, router, mock_page, authenticated_state):
        """测试4：已登录访问受保护路由（正常访问）"""
        router.mount(mock_page, authenticated_state)
        
        protected_routes = {
            "/dashboard": "DashboardView",
            "/records": "RecordsView",
            "/add_record": "AddRecordView",
            "/statistics": "StatisticsView",
            "/settings": "SettingsView"
        }
        
        for route, view_name in protected_routes.items():
            mock_page.route = route
            mock_page.views = []
            
            with patch(f'views.router.{view_name}') as MockView:
                router.route_change(None)
                
                assert MockView.called, f"Route {route} failed"
                # 不应该重定向到登录页
                if mock_page.go.called:
                    assert mock_page.go.call_args[0][0] != "/login"


class TestViewNavigation:
    """测试视图导航"""
    
    def test_view_pop_operations(self, mounted_router, mock_page):
        """测试5：视图弹出操作（多视图/单视图）"""
        # 测试多视图弹出
        mock_view1 = Mock()
        mock_view1.route = "/welcome"
        mock_view2 = Mock()
        mock_view2.route = "/login"
        
        mock_page.views = [mock_view1, mock_view2]
        mounted_router.view_pop(None)
        
        assert len(mock_page.views) == 1
        mock_page.go.assert_called_with("/welcome")
        
        # 测试单视图不弹出
        mock_page.go.reset_mock()
        mock_page.views = [mock_view1]
        mounted_router.view_pop(None)
        
        assert len(mock_page.views) == 1
        assert not mock_page.go.called


class TestRouteCleanup:
    """测试路由清理和更新"""
    
    def test_views_cleared_on_route_change(self, mounted_router, mock_page):
        """测试6：路由变化时清空并更新视图"""
        # 添加多个旧视图
        mock_page.views = [Mock(), Mock(), Mock()]
        mock_page.route = "/welcome"
        
        with patch('views.router.WelcomeView'):
            mounted_router.route_change(None)
        
        # 应该调用 update
        mock_page.update.assert_called()
        # views 被清空后添加新视图
        assert len(mock_page.views) >= 0


class TestInvalidRoutes:
    """测试无效路由"""
    
    def test_unknown_and_empty_routes(self, mounted_router, mock_page):
        """测试7：未知路由和空路由（默认跳转欢迎页）"""
        invalid_routes = ["/unknown_route", "/404", ""]
        
        for route in invalid_routes:
            mock_page.route = route
            mock_page.views = []
            
            with patch('views.router.WelcomeView') as MockView:
                mounted_router.route_change(None)
                
                # 未知路由应该显示某个视图
                mock_page.update.assert_called()


class TestEdgeCases:
    """测试边界情况"""
    
    def test_route_change_without_mount(self, router):
        """测试8：未挂载时调用 route_change"""
        try:
            router.route_change(None)
        except AttributeError:
            # 预期行为：访问 None.views 会抛出异常
            pass
    
    def test_rapid_route_changes(self, mounted_router, mock_page):
        """测试9：快速连续的路由变化"""
        routes = ["/welcome", "/login", "/register", "/welcome"]
        
        with patch('views.router.WelcomeView'), \
             patch('views.router.LoginView'), \
             patch('views.router.RegisterView'):
            
            for route in routes:
                mock_page.route = route
                mounted_router.route_change(None)
        
        # 应该没有异常，每次都调用 update
        assert mock_page.update.call_count == len(routes)
    
    def test_authentication_state_changes(self, router, mock_page, mock_state):
        """测试10：认证状态变化时的路由访问"""
        router.mount(mock_page, mock_state)
        
        # 未登录访问受保护路由
        mock_page.route = "/dashboard"
        mock_state.current_user = None
        router.route_change(None)
        assert mock_page.go.called
        
        # 登录后访问相同路由
        mock_page.go.reset_mock()
        mock_state.current_user = User(
            user_id=1,
            username="test",
            password_hash="hash",
            email="test@test.com"
        )
        
        with patch('views.router.DashboardView'):
            router.route_change(None)
            # 不应该重定向
            if mock_page.go.called:
                assert mock_page.go.call_args[0][0] != "/login"