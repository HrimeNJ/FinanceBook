"""
Router for ui change
"""

import flet as ft

from views.add_record import AddRecordView
from views.dashboard import DashboardView
from views.login import LoginView
from views.records import RecordsView
from views.register import RegisterView
from views.settings import SettingsView
from views.statistics import StatisticsView
from views.welcome import WelcomeView


class Router:
    """路由控制器"""

    def __init__(self):
        self.page = None
        self.state = None

    def mount(self, page: ft.Page, state):
        """挂载路由到页面"""
        self.page = page
        self.state = state
        page.on_route_change = self.route_change
        page.on_view_pop = self.view_pop

    def route_change(self, e):
        """路由变化处理"""
        self.page.views.clear()

        # 检查需要登录的路由
        protected_routes = [
            "/dashboard",
            "/records",
            "/add_record",
            "/statistics",
            "/settings",
        ]
        if self.page.route in protected_routes and not self.state.current_user:
            self.page.go("/login")
            return

        match self.page.route:
            case "/welcome" | "/":
                self.page.views.append(WelcomeView(self.state, self.page.go))
            case "/login":
                self.page.views.append(LoginView(self.state, self.page.go))
            case "/register":
                self.page.views.append(RegisterView(self.state, self.page.go))
            case "/dashboard":
                self.page.views.append(DashboardView(self.state, self.page.go))
            case "/records":
                self.page.views.append(RecordsView(self.state, self.page.go))
            case "/add_record":
                self.page.views.append(AddRecordView(self.state, self.page.go))
            case "/statistics":
                self.page.views.append(StatisticsView(self.state, self.page.go))
            case "/settings":
                self.page.views.append(SettingsView(self.state, self.page.go))
            case _:
                self.page.views.append(WelcomeView(self.state, self.page.go))

        self.page.update()

    def view_pop(self, s):
        """视图弹出处理"""
        if len(self.page.views) > 1:
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
