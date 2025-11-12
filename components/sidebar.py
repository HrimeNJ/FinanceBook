"""
Sidebar component for the application
"""

import flet as ft


class Sidebar:
    """侧边栏组件"""

    def __init__(self, page, current_user, on_logout, on_navigate):
        self.page = page
        self.current_user = current_user
        self.on_logout = on_logout
        self.on_navigate = on_navigate

    def create_sidebar(self):
        """创建侧边栏"""
        # Logo区域
        logo_section = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        ft.Icons.ACCOUNT_BALANCE_WALLET, size=32, color=ft.Colors.BLUE
                    ),
                    ft.Text(
                        "理财记账本",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_800,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.padding.symmetric(vertical=20),
            alignment=ft.alignment.center,
        )

        # 用户信息区域
        user_section = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.ACCOUNT_CIRCLE, size=50, color=ft.Colors.GREY_600
                        ),
                        bgcolor=ft.Colors.GREY_200,
                        border_radius=25,
                        padding=ft.padding.all(8),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        (
                            f"您好, {self.current_user.username}"
                            if self.current_user
                            else "访客"
                        ),
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_800,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        self.current_user.email if self.current_user else "",
                        size=12,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.padding.all(16),
            margin=ft.margin.symmetric(horizontal=16),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
        )

        # 导航菜单
        nav_items = [
            ("仪表盘", ft.Icons.DASHBOARD, "/dashboard"),
            ("添加记录", ft.Icons.ADD_CIRCLE, "/add_record"),
            ("记录列表", ft.Icons.LIST_ALT, "/records"),
            ("统计列表", ft.Icons.ANALYTICS, "/statistics"),
            ("设置", ft.Icons.SETTINGS, "/settings"),
        ]

        nav_buttons = []
        for text, icon, route in nav_items:
            is_active = self.page.route == route
            btn = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            icon,
                            size=20,
                            color=(
                                ft.Colors.BLUE_700 if is_active else ft.Colors.GREY_700
                            ),
                        ),
                        ft.Text(
                            text,
                            size=14,
                            color=(
                                ft.Colors.BLUE_700 if is_active else ft.Colors.GREY_700
                            ),
                            weight=(
                                ft.FontWeight.BOLD if is_active else ft.FontWeight.W_500
                            ),
                        ),
                    ],
                    spacing=12,
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                margin=ft.margin.symmetric(horizontal=8, vertical=2),
                border_radius=8,
                bgcolor=ft.Colors.BLUE_50 if is_active else None,
                ink=True,
                on_click=lambda e, r=route: self.on_navigate(r),
            )
            nav_buttons.append(btn)

        # 底部区域
        bottom_section = ft.Column(
            [
                ft.Switch(
                    label="深色模式",
                    value=self.page.theme_mode == ft.ThemeMode.DARK,
                    on_change=self.toggle_theme,
                ),
                ft.Container(height=16),
                ft.ElevatedButton(
                    text="退出登录",
                    icon=ft.Icons.LOGOUT,
                    width=200,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_100,
                        color=ft.Colors.RED_700,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=self.handle_logout,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        )

        return ft.Container(
            content=ft.Column(
                [
                    logo_section,
                    user_section,
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column(nav_buttons, spacing=4),
                        expand=True,
                    ),
                    ft.Container(
                        content=bottom_section,
                        padding=ft.padding.all(16),
                    ),
                ],
                spacing=0,
            ),
            width=280,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_200)),
            padding=0,
        )

    def toggle_theme(self, e):
        """切换主题"""
        if e.control.value:
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.update()

    def handle_logout(self, e):
        """处理登出"""
        if self.on_logout:
            self.on_logout(e)
