"""
LoginView for ui
"""

import hashlib

import flet as ft

from models.user import User


class LoginView(ft.View):
    """登录视图"""

    def __init__(self, state, go):
        super().__init__(route="/login")
        self.state = state
        self.go = go
        self.page = state.page

        # 创建登录界面
        self.create_login_components()
        self.controls = [self.create_login_layout()]

    def create_login_components(self):
        """创建登录组件"""
        # 用户名输入
        self.username_field = ft.TextField(
            label="用户名",
            width=320,
            height=60,
            prefix_icon=ft.Icons.PERSON,
            border_radius=12,
            on_submit=self.handle_login,
        )

        # 密码输入
        self.password_field = ft.TextField(
            label="密码",
            width=320,
            height=60,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=12,
            on_submit=self.handle_login,
        )

        # 登录按钮
        self.login_btn = ft.ElevatedButton(
            text="登录",
            width=320,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
            ),
            on_click=self.handle_login,
        )

    def create_login_layout(self):
        """创建登录布局"""
        # 注册按钮
        register_btn = ft.TextButton(
            text="创建新账户",
            width=320,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            on_click=lambda e: self.go("/register"),
        )

        # 主题切换
        theme_switch = ft.Switch(
            label="深色模式",
            value=False,  # 可以从 state 中获取
            on_change=self.toggle_theme,
        )

        # 右侧登录表单
        login_form = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=40),
                    ft.Text(
                        "欢迎回来",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_900,
                    ),
                    ft.Text(
                        "请登录您的账户",
                        size=16,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Container(height=40),
                    self.username_field,
                    ft.Container(height=16),
                    self.password_field,
                    ft.Container(height=24),
                    self.login_btn,
                    ft.Container(height=16),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    ft.Container(height=8),
                    register_btn,
                    ft.Container(height=20),
                    theme_switch,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(40),
            expand=1,
            alignment=ft.alignment.center,
        )

        # 左侧装饰面板
        left_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(
                                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                                    size=80,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "理财记账本",
                                    size=36,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    "您的个人财务管家\n记录 • 分析 • 优化",
                                    size=16,
                                    color=ft.Colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                self.create_feature_item("TRENDING_UP", "支出追踪"),
                                self.create_feature_item("ANALYTICS", "财务分析"),
                                self.create_feature_item("SAVE_ALT", "数据导出"),
                                self.create_feature_item("SECURITY", "安全存储"),
                            ],
                            spacing=12,
                        ),
                        padding=ft.padding.only(bottom=40),
                    ),
                ]
            ),
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=ft.padding.all(40),
            expand=1,
        )

        return ft.Row([left_panel, login_form], spacing=0, expand=True)

    def handle_login(self, e):
        """处理登录"""
        username = self.username_field.value
        password = self.password_field.value

        if not username or not password:
            self.show_snackbar("请输入用户名和密码", "error")
            return

        # 显示加载状态
        self.login_btn.text = "登录中..."
        self.login_btn.disabled = True
        self.page.update()

        try:
            # 查询用户
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user_data = self.state.db.query(
                "SELECT * FROM users WHERE username = ?", (username,)
            )

            if not user_data:
                self.show_snackbar("用户不存在", "error")
                return

            user_dict = user_data[0]
            user = User.from_dict(user_dict)

            # 验证密码
            if user.password_hash == password_hash:
                self.state.set_current_user(user)
                self.show_snackbar("登录成功", "success")
                self.go("/dashboard")
            else:
                self.show_snackbar("密码错误", "error")

        except Exception as ex:
            self.show_snackbar(f"登录失败: {ex}", "error")
        finally:
            # 恢复按钮状态
            self.login_btn.text = "登录"
            self.login_btn.disabled = False
            self.page.update()

    def toggle_theme(self, e):
        """切换主题"""
        if e.control.value:
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.update()

    def create_feature_item(self, icon_name, text):
        """创建特性项目"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        getattr(ft.Icons, icon_name), size=20, color=ft.Colors.WHITE
                    ),
                    ft.Text(text, size=14, color=ft.Colors.WHITE),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(vertical=4),
        )

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
