"""
FinanceBook Desktop Application Main Class

This module contains the main FinanceBook application class for Flet desktop app
that orchestrates all components, models, and views.
"""

from typing import Optional

import flet as ft

from models.app_state import AppState
from models.database import DatabaseManager
from views.router import Router


class FinanceBookApp:
    """
    Main FinanceBook Desktop Application Class

    Handles application initialization, state management, and routing for Flet desktop app.
    """

    def __init__(self, db_path: str = "finance_book.db"):
        """
        初始化 FinanceBook 桌面应用

        Args:
            db_path (str): 数据库文件路径
        """
        self.db_path = db_path
        self.db_manager: Optional[DatabaseManager] = None
        self.app_state: Optional[AppState] = None
        self.router: Optional[Router] = None
        self.page: Optional[ft.Page] = None

    def _initialize_app(self):
        """初始化应用组件"""
        try:
            # 初始化数据库
            self.db_manager = DatabaseManager(self.db_path)
            print("数据库初始化成功")

            # 初始化应用状态
            self.app_state = AppState(self.db_manager, self.page)
            print("应用状态初始化成功")

            # 初始化路由
            self.router = Router()
            self.router.mount(self.page, self.app_state)
            print("路由器初始化成功")

        except Exception as e:
            print(f"应用初始化失败: {e}")
            # 显示错误信息给用户
            if self.page:
                self.page.add(
                    ft.Text(
                        f"应用初始化失败: {e}",
                        size=16,
                        color=ft.Colors.RED,
                    )
                )

    def _configure_app(self):
        """配置 Flet 应用"""
        if not self.page:
            raise ValueError("Page对象不能为空")

        # 设置应用基本属性
        self.page.title = "FinanceBook - 个人理财管理"
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.window.center()
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0

        # 设置应用主题
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.BLUE_700,
                primary_container=ft.Colors.BLUE_100,
                secondary=ft.Colors.GREEN_600,
                secondary_container=ft.Colors.GREEN_100,
                surface=ft.Colors.WHITE,
                background=ft.Colors.GREY_50,
            )
        )

        # 设置字体
        self.page.fonts = {
            "NotoSansSC": "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap"
        }

        print("应用配置完成")

    def main(self, page: ft.Page):
        """
        应用主入口点

        Args:
            page (ft.Page): Flet页面对象
        """
        self.page = page

        try:
            # 配置应用
            self._configure_app()

            # 初始化应用组件
            self._initialize_app()

            # 导航到欢迎页面
            self.page.go("/welcome")

            print("FinanceBook应用启动成功!")

        except Exception as e:
            print(f"应用启动失败: {e}")
            # 显示错误页面
            self.page.add(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.ERROR, size=64, color=ft.Colors.RED),
                            ft.Text("应用启动失败", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"错误信息: {e}", size=14, color=ft.Colors.GREY_600
                            ),
                            ft.ElevatedButton(
                                "重新启动",
                                on_click=lambda e: self.page.window_destroy(),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
