"""
WelcomeView for ui
"""

import flet as ft


class WelcomeView(ft.View):
    """欢迎视图"""

    def __init__(self, state, go):
        super().__init__(route="/welcome")
        self.state = state
        self.go = go
        self.controls = [self.create_welcome_layout()]

    def create_welcome_layout(self):
        """创建欢迎布局"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(
                                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                                    size=120,
                                    color=ft.Colors.BLUE_600,
                                ),
                                ft.Text(
                                    "理财记账本",
                                    size=48,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_900,
                                ),
                                ft.Text(
                                    "您的个人财务管家",
                                    size=20,
                                    color=ft.Colors.GREY_600,
                                ),
                                ft.Container(height=40),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            text="登录",
                                            width=160,
                                            height=50,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.BLUE_600,
                                                color=ft.Colors.WHITE,
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=12
                                                ),
                                                text_style=ft.TextStyle(
                                                    size=16, weight=ft.FontWeight.BOLD
                                                ),
                                            ),
                                            on_click=lambda e: self.go("/login"),
                                        ),
                                        ft.ElevatedButton(
                                            text="注册",
                                            width=160,
                                            height=50,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.GREEN_600,
                                                color=ft.Colors.WHITE,
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=12
                                                ),
                                                text_style=ft.TextStyle(
                                                    size=16, weight=ft.FontWeight.BOLD
                                                ),
                                            ),
                                            on_click=lambda e: self.go("/register"),
                                        ),
                                    ],
                                    spacing=20,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                ],
                expand=True,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_50, ft.Colors.GREEN_50],
            ),
            expand=True,
        )
