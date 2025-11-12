"""
RegisterView for ui
"""

import hashlib

import flet as ft

from models.user import User


class RegisterView(ft.View):
    """注册视图"""

    def __init__(self, state, go):
        super().__init__(route="/register")
        self.state = state
        self.go = go
        self.page = state.page

        # 创建注册界面
        self.create_register_components()
        self.controls = [self.create_register_layout()]

    def create_register_components(self):
        """创建注册组件"""
        # 表单字段
        self.reg_username = ft.TextField(
            label="用户名 *",
            width=300,
            height=60,
            prefix_icon=ft.Icons.PERSON,
            border_radius=12,
        )

        self.reg_email = ft.TextField(
            label="邮箱地址 *",
            width=300,
            height=60,
            prefix_icon=ft.Icons.EMAIL,
            border_radius=12,
        )

        self.reg_password = ft.TextField(
            label="密码 *",
            width=300,
            height=60,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=12,
        )

        self.reg_confirm_password = ft.TextField(
            label="确认密码 *",
            width=300,
            height=60,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            border_radius=12,
            on_submit=self.handle_register,
        )

        # 注册按钮
        self.register_btn = ft.ElevatedButton(
            text="创建账户",
            width=300,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
            ),
            on_click=self.handle_register,
        )

    def create_register_layout(self):
        """创建注册布局"""
        # 返回按钮
        back_btn = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            tooltip="返回登录",
            on_click=lambda e: self.go("/login"),
        )

        content = ft.Column(
            [
                ft.Row([back_btn], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=20),
                ft.Text(
                    "创建账户",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900,
                ),
                ft.Text("加入理财记账本", size=16, color=ft.Colors.GREY_600),
                ft.Container(height=40),
                # 基本信息部分
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "基本信息",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Container(height=16),
                            self.reg_username,
                            ft.Container(height=16),
                            self.reg_email,
                        ]
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=12,
                    width=340,
                ),
                ft.Container(height=20),
                # 安全信息部分
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "账户安全",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Container(height=16),
                            self.reg_password,
                            ft.Container(height=16),
                            self.reg_confirm_password,
                            ft.Container(height=8),
                            ft.Text(
                                "请使用字母、数字和符号的组合",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ]
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=12,
                    width=340,
                ),
                ft.Container(height=30),
                self.register_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.Container(
            content=content,
            padding=ft.padding.all(40),
            alignment=ft.alignment.center,
            expand=True,
        )

    def handle_register(self, e):
        """处理注册"""
        username = self.reg_username.value
        email = self.reg_email.value
        password = self.reg_password.value
        confirm_password = self.reg_confirm_password.value

        # 验证输入
        if not all([username, email, password, confirm_password]):
            self.show_snackbar("请填写所有必填字段", "error")
            return

        if password != confirm_password:
            self.show_snackbar("密码不匹配", "error")
            return

        if len(password) < 6:
            self.show_snackbar("密码至少需要6个字符", "error")
            return

        # 显示加载状态
        self.register_btn.text = "创建账户中..."
        self.register_btn.disabled = True
        self.page.update()

        try:
            # 检查用户名和邮箱是否已存在
            existing_user = self.state.db.query(
                "SELECT user_id FROM users WHERE username = ? OR email = ?",
                (username, email),
            )

            if existing_user:
                self.show_snackbar("用户名或邮箱已存在", "error")
                return

            # 注册用户
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = User(username=username, password_hash=password_hash, email=email)

            # 保存用户到数据库
            success = self.state.db.save_user(user)

            if success:
                self.show_snackbar("账户创建成功！", "success")
                # 延迟跳转到登录页面
                self.page.run_thread(lambda: self.delayed_redirect_to_login())
            else:
                self.show_snackbar("注册失败，请重试", "error")

        except Exception as ex:
            self.show_snackbar(f"注册失败: {ex}", "error")
        finally:
            # 恢复按钮状态
            self.register_btn.text = "创建账户"
            self.register_btn.disabled = False
            self.page.update()

    def delayed_redirect_to_login(self):
        """延迟跳转到登录页面"""
        import time

        time.sleep(1)  # 等待1秒
        self.go("/login")

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
