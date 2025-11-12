"""
SettingsView for ui
"""

import flet as ft

from components.sidebar import Sidebar
from models.export import ExportModule


class SettingsView(ft.View):
    """设置视图"""

    def __init__(self, state, go):
        super().__init__(route="/settings")
        self.state = state
        self.go = go
        self.page = state.page
        self.export_module = ExportModule(state)
        self.create_settings_components()
        self.controls = [self.create_settings_layout()]

    def create_settings_components(self):
        """创建设置组件"""
        # 用户信息设置
        self.settings_username = ft.TextField(
            label="用户名",
            value=self.state.current_user.username if self.state.current_user else "",
            width=300,
        )

        self.settings_email = ft.TextField(
            label="邮箱",
            value=self.state.current_user.email if self.state.current_user else "",
            width=300,
        )

        # 应用设置
        self.currency_dropdown = ft.Dropdown(
            label="货币",
            width=200,
            options=[
                ft.dropdown.Option("CNY", "人民币 (¥)"),
                ft.dropdown.Option("USD", "美元 ($)"),
                ft.dropdown.Option("EUR", "欧元 (€)"),
                ft.dropdown.Option("GBP", "英镑 (£)"),
            ],
            value="CNY",
        )

        self.theme_switch = ft.Switch(
            label="深色模式",
            value=False,
            on_change=self.toggle_theme,
        )

        self.notifications_switch = ft.Switch(
            label="启用通知",
            value=True,
        )

    def create_settings_layout(self):
        """创建设置布局"""
        # 侧边栏
        sidebar = Sidebar(
            self.page, self.state.current_user, self.handle_logout, self.go
        ).create_sidebar()

        # 主内容
        main_content = ft.Container(
            content=ft.Column(
                [
                    # 页面标题 - 固定在顶部
                    self.create_page_header("设置"),
                    # 可滚动的内容区域
                    ft.Container(
                        content=ft.Column(
                            [
                                # 用户配置
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Icon(
                                                        ft.Icons.PERSON,
                                                        size=24,
                                                        color=ft.Colors.BLUE_600,
                                                    ),
                                                    ft.Text(
                                                        "账户设置",
                                                        size=18,
                                                        weight=ft.FontWeight.W_600,
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Divider(
                                                height=20, color=ft.Colors.GREY_300
                                            ),
                                            ft.ResponsiveRow(
                                                [
                                                    ft.Container(
                                                        content=ft.Column(
                                                            [
                                                                self.settings_username,
                                                                ft.Container(height=16),
                                                                self.settings_email,
                                                            ]
                                                        ),
                                                        col={"sm": 12, "md": 8},
                                                    ),
                                                    ft.Container(
                                                        content=ft.Column(
                                                            [
                                                                ft.ElevatedButton(
                                                                    text="修改密码",
                                                                    icon=ft.Icons.LOCK,
                                                                    style=ft.ButtonStyle(
                                                                        bgcolor=ft.Colors.ORANGE_600,
                                                                        color=ft.Colors.WHITE,
                                                                        shape=ft.RoundedRectangleBorder(
                                                                            radius=8
                                                                        ),
                                                                    ),
                                                                    on_click=self.change_password,
                                                                ),
                                                                ft.Container(height=16),
                                                                ft.ElevatedButton(
                                                                    text="更新资料",
                                                                    icon=ft.Icons.SAVE,
                                                                    style=ft.ButtonStyle(
                                                                        bgcolor=ft.Colors.BLUE_600,
                                                                        color=ft.Colors.WHITE,
                                                                        shape=ft.RoundedRectangleBorder(
                                                                            radius=8
                                                                        ),
                                                                    ),
                                                                    on_click=self.update_profile,
                                                                ),
                                                            ]
                                                        ),
                                                        col={"sm": 12, "md": 4},
                                                    ),
                                                ],
                                                spacing=20,
                                            ),
                                        ]
                                    ),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.all(25),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                    border=ft.border.all(1, ft.Colors.GREY_200),
                                ),
                                # 应用设置
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Icon(
                                                        ft.Icons.SETTINGS,
                                                        size=24,
                                                        color=ft.Colors.GREEN_600,
                                                    ),
                                                    ft.Text(
                                                        "应用偏好",
                                                        size=18,
                                                        weight=ft.FontWeight.W_600,
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Divider(
                                                height=20, color=ft.Colors.GREY_300
                                            ),
                                            ft.ResponsiveRow(
                                                [
                                                    ft.Container(
                                                        content=ft.Column(
                                                            [
                                                                ft.Text(
                                                                    "显示设置",
                                                                    size=14,
                                                                    weight=ft.FontWeight.W_500,
                                                                ),
                                                                ft.Container(height=8),
                                                                self.currency_dropdown,
                                                                ft.Container(height=16),
                                                                self.theme_switch,
                                                                ft.Container(height=16),
                                                                self.notifications_switch,
                                                            ]
                                                        ),
                                                        col={"sm": 12, "md": 6},
                                                    ),
                                                    ft.Container(
                                                        content=ft.Column(
                                                            [
                                                                ft.Text(
                                                                    "数据管理",
                                                                    size=14,
                                                                    weight=ft.FontWeight.W_500,
                                                                ),
                                                                ft.Container(height=8),
                                                                ft.ElevatedButton(
                                                                    text="导出数据",
                                                                    icon=ft.Icons.DOWNLOAD,
                                                                    style=ft.ButtonStyle(
                                                                        bgcolor=ft.Colors.GREEN_600,
                                                                        color=ft.Colors.WHITE,
                                                                        shape=ft.RoundedRectangleBorder(
                                                                            radius=8
                                                                        ),
                                                                    ),
                                                                    width=160,
                                                                    on_click=self.export_all_data,
                                                                ),
                                                                ft.Container(height=12),
                                                                ft.ElevatedButton(
                                                                    text="导入数据",
                                                                    icon=ft.Icons.UPLOAD,
                                                                    style=ft.ButtonStyle(
                                                                        bgcolor=ft.Colors.CYAN_600,
                                                                        color=ft.Colors.WHITE,
                                                                        shape=ft.RoundedRectangleBorder(
                                                                            radius=8
                                                                        ),
                                                                    ),
                                                                    width=160,
                                                                    on_click=self.import_data,
                                                                ),
                                                                ft.Container(height=12),
                                                                ft.ElevatedButton(
                                                                    text="重置应用",
                                                                    icon=ft.Icons.RESTORE,
                                                                    style=ft.ButtonStyle(
                                                                        bgcolor=ft.Colors.RED_600,
                                                                        color=ft.Colors.WHITE,
                                                                        shape=ft.RoundedRectangleBorder(
                                                                            radius=8
                                                                        ),
                                                                    ),
                                                                    width=160,
                                                                    on_click=self.reset_app_data,
                                                                ),
                                                            ]
                                                        ),
                                                        col={"sm": 12, "md": 6},
                                                    ),
                                                ],
                                                spacing=20,
                                            ),
                                        ]
                                    ),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.all(25),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                    border=ft.border.all(1, ft.Colors.GREY_200),
                                ),
                                # 关于信息
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "关于理财记账本",
                                                size=18,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            ft.Container(height=12),
                                            ft.Text(
                                                "版本 1.0.0",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Text(
                                                "个人财务管理应用",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Container(height=16),
                                            ft.Row(
                                                [
                                                    ft.TextButton(
                                                        text="隐私政策",
                                                        on_click=lambda e: self.show_privacy_policy(),
                                                    ),
                                                    ft.Text(
                                                        "•", color=ft.Colors.GREY_400
                                                    ),
                                                    ft.TextButton(
                                                        text="服务条款",
                                                        on_click=lambda e: self.show_terms(),
                                                    ),
                                                    ft.Text(
                                                        "•", color=ft.Colors.GREY_400
                                                    ),
                                                    ft.TextButton(
                                                        text="支持",
                                                        on_click=lambda e: self.show_support(),
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                        ]
                                    ),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.all(25),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                    border=ft.border.all(1, ft.Colors.GREY_200),
                                ),
                                # 底部留白
                                ft.Container(height=50),
                            ],
                            spacing=0,
                            scroll=ft.ScrollMode.AUTO,  # 启用滚动
                        ),
                        expand=True,  # 占满剩余空间
                    ),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.GREY_50,
            expand=True,
            padding=0,
        )

        return ft.Row([sidebar, main_content], spacing=0, expand=True)

    def create_page_header(self, title, subtitle=""):
        """创建页面标题"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        title,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_900,
                    ),
                    (
                        ft.Text(subtitle, size=16, color=ft.Colors.GREY_600)
                        if subtitle
                        else ft.Container()
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=30, vertical=30),
        )

    def toggle_theme(self, e):
        """切换主题"""
        if e.control.value:
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.update()

    def change_password(self, e):
        """修改密码"""
        self.show_snackbar("修改密码功能将在后续版本实现", "info")

    def update_profile(self, e):
        """更新个人资料"""
        self.show_snackbar("个人资料更新功能将在后续版本实现", "info")

    def export_all_data(self, e):
        """导出所有数据"""
        # 创建导出格式选择对话框
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        def export_json(e):
            close_dialog(e)
            success, result = self.export_module.export_to_json()
            if success:
                self.show_snackbar(f"JSON导出成功: {result}", "success")
            else:
                self.show_snackbar(result, "error")

        def export_excel(e):
            close_dialog(e)
            success, result = self.export_module.export_to_excel()
            if success:
                self.show_snackbar(f"Excel导出成功: {result}", "success")
            else:
                self.show_snackbar(result, "error")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("选择导出格式"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("请选择要导出的文件格式:", size=14),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            text="导出为 JSON",
                            icon=ft.Icons.CODE,
                            width=200,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                            ),
                            on_click=export_json,
                        ),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            text="导出为 Excel",
                            icon=ft.Icons.TABLE_CHART,
                            width=200,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                            ),
                            on_click=export_excel,
                        ),
                    ],
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=300,
            ),
            actions=[
                ft.TextButton("取消", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def import_data(self, e):
        """导入数据"""
        self.show_snackbar("导入数据功能将在后续版本实现", "info")

    def reset_app_data(self, e):
        """重置应用数据"""
        self.show_snackbar("重置应用功能将在后续版本实现", "info")

    def show_privacy_policy(self):
        """显示隐私政策"""
        self.show_snackbar("隐私政策页面将在后续版本实现", "info")

    def show_terms(self):
        """显示服务条款"""
        self.show_snackbar("服务条款页面将在后续版本实现", "info")

    def show_support(self):
        """显示支持信息"""
        self.show_snackbar("支持页面将在后续版本实现", "info")

    def handle_logout(self, e):
        """处理登出"""
        self.state.clear_user_data()
        self.go("/welcome")

    def show_snackbar(self, message: str, message_type: str = "info"):
        """显示提示消息"""
        Colors = {
            "success": ft.Colors.GREEN,
            "error": ft.Colors.RED,
            "info": ft.Colors.BLUE,
        }

        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=Colors.get(message_type, ft.Colors.BLUE),
            show_close_icon=True,
        )

        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()
