"""
AddRecordView for ui
"""

from datetime import datetime

import flet as ft

from components.sidebar import Sidebar
from models.record import Record


class AddRecordView(ft.View):
    """添加记录视图"""

    def __init__(self, state, go):
        super().__init__(route="/add_record")
        self.state = state
        self.go = go
        self.page = state.page

        # 创建组件
        self.create_form_components()
        self.load_categories("expense")  # 默认加载支出分类

        # 创建布局
        self.controls = [self.create_add_record_layout()]

    def create_form_components(self):
        """创建表单组件"""
        # 类型选择
        self.record_type = ft.Dropdown(
            label="类型",
            width=200,
            options=[
                ft.dropdown.Option("income", "收入"),
                ft.dropdown.Option("expense", "支出"),
            ],
            value="expense",
            on_change=self.on_record_type_change,
        )

        # 金额输入
        self.amount_field = ft.TextField(
            label="金额",
            width=200,
            prefix_text="¥",
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        # 分类选择
        self.category_dropdown = ft.Dropdown(
            label="分类",
            width=200,
            options=[],
        )

        # 描述输入
        self.description_field = ft.TextField(
            label="备注",
            width=400,
            multiline=True,
            max_lines=3,
        )

        # 日期选择
        self.date_picker = ft.DatePicker(
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2030, 12, 31),
            on_change=self.on_date_change,
        )

        self.selected_date = ft.TextField(
            label="日期",
            width=200,
            value=datetime.now().strftime("%Y-%m-%d"),
            read_only=True,
            suffix=ft.IconButton(
                icon=ft.Icons.CALENDAR_TODAY,
                on_click=lambda e: self.page.open(self.date_picker),
            ),
        )

    def create_add_record_layout(self):
        """创建添加记录布局"""
        # 侧边栏
        sidebar = Sidebar(
            self.page, self.state.current_user, self.handle_logout, self.go
        ).create_sidebar()

        # 主内容
        main_content = ft.Container(
            content=ft.Column(
                [
                    self.create_page_header("添加新记录"),
                    # 表单卡片
                    ft.Container(
                        content=ft.Column(
                            [
                                # 表单标题
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.ADD_CIRCLE_OUTLINE,
                                            size=24,
                                            color=ft.Colors.BLUE_600,
                                        ),
                                        ft.Text(
                                            "新交易记录",
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.GREY_800,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                ft.Divider(height=20, color=ft.Colors.GREY_300),
                                # 表单字段
                                ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    "基本信息",
                                                    size=16,
                                                    weight=ft.FontWeight.W_600,
                                                ),
                                                ft.Container(height=8),
                                                self.record_type,
                                                ft.Container(height=16),
                                                self.amount_field,
                                                ft.Container(height=16),
                                                self.category_dropdown,
                                            ],
                                            spacing=0,
                                        ),
                                        ft.VerticalDivider(width=40),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    "详细信息",
                                                    size=16,
                                                    weight=ft.FontWeight.W_600,
                                                ),
                                                ft.Container(height=8),
                                                self.selected_date,
                                                ft.Container(height=16),
                                                self.description_field,
                                            ],
                                            spacing=0,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=40,
                                ),
                                ft.Container(height=30),
                                # 操作按钮
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            text="取消",
                                            style=ft.ButtonStyle(
                                                color=ft.Colors.GREY_700,
                                                bgcolor=ft.Colors.GREY_200,
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=8
                                                ),
                                            ),
                                            width=120,
                                            on_click=lambda e: self.go("/dashboard"),
                                        ),
                                        ft.ElevatedButton(
                                            text="保存记录",
                                            icon=ft.Icons.SAVE,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.BLUE_600,
                                                color=ft.Colors.WHITE,
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=8
                                                ),
                                            ),
                                            width=140,
                                            on_click=self.save_record,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                    spacing=16,
                                ),
                            ],
                            spacing=0,
                        ),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=16,
                        padding=ft.padding.all(30),
                        margin=ft.margin.all(20),
                        border=ft.border.all(1, ft.Colors.GREY_200),
                    ),
                    # 快速操作
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "快速操作", size=16, weight=ft.FontWeight.W_600
                                ),
                                ft.Container(height=12),
                                ft.Row(
                                    [
                                        self.create_quick_action_card(
                                            "咖啡",
                                            "5.50",
                                            ft.Icons.LOCAL_CAFE,
                                            ft.Colors.BROWN,
                                        ),
                                        self.create_quick_action_card(
                                            "午餐",
                                            "12.00",
                                            ft.Icons.RESTAURANT,
                                            ft.Colors.ORANGE,
                                        ),
                                        self.create_quick_action_card(
                                            "交通",
                                            "3.20",
                                            ft.Icons.DIRECTIONS_BUS,
                                            ft.Colors.BLUE,
                                        ),
                                        self.create_quick_action_card(
                                            "购物",
                                            "45.00",
                                            ft.Icons.SHOPPING_CART,
                                            ft.Colors.GREEN,
                                        ),
                                    ],
                                    spacing=16,
                                ),
                            ]
                        ),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=16,
                        padding=ft.padding.all(20),
                        margin=ft.margin.symmetric(horizontal=20),
                        border=ft.border.all(1, ft.Colors.GREY_200),
                    ),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.GREY_50,
            expand=True,
            padding=0,
        )

        # 添加日期选择器到页面
        self.page.overlay.append(self.date_picker)

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

    def create_quick_action_card(self, title, amount, icon, color):
        """创建快速操作卡片"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=24, color=color),
                    ft.Text(title, size=12, weight=ft.FontWeight.W_500),
                    ft.Text(f"¥{amount}", size=14, weight=ft.FontWeight.BOLD),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, color),
            border_radius=8,
            padding=ft.padding.all(12),
            width=100,
            height=80,
            ink=True,
            on_click=lambda e, a=amount, t=title: self.quick_fill(a, t),
        )

    def quick_fill(self, amount, title):
        """快速填充表单"""
        self.amount_field.value = amount
        self.description_field.value = title
        self.page.update()

    def on_record_type_change(self, e):
        """记录类型改变时更新分类"""
        self.load_categories(e.control.value)

    def on_date_change(self, e):
        """日期改变"""
        self.selected_date.value = e.control.value.strftime("%Y-%m-%d")
        self.page.update()

    def load_categories(self, record_type):
        """加载分类选项"""
        categories = self.state.db.get_categories()
        self.category_dropdown.options = [
            ft.dropdown.Option(str(cat.category_id), cat.name) for cat in categories
        ]
        self.page.update()

    def save_record(self, e):
        """保存记录"""
        try:
            if not all(
                [
                    self.amount_field.value,
                    self.record_type.value,
                    self.category_dropdown.value,
                ]
            ):
                self.show_snackbar("请填写所有必要字段", "error")
                return

            amount = float(self.amount_field.value)
            selected_type = self.record_type.value
            category_id = int(self.category_dropdown.value)
            note = self.description_field.value or ""
            record_date = datetime.strptime(self.selected_date.value, "%Y-%m-%d")

            # BUG: 直接访问 current_user 而不检查是否为 None
            # if not self.state.current_user:
            #     self.show_snackbar("会话已过期", "error")
            #     return

            # 在访问.user_id 属性时，如果 current_user 是 None 会触发:
            # AttributeError: 'NoneType' object has no attribute 'user_id'
            record = Record(
                amount=amount,
                record_type=selected_type,
                category_id=category_id,
                note=note,
                user_id=self.state.current_user.user_id,
                date=record_date,
            )

            if self.state.add_record(record):
                self.show_snackbar("记录保存成功", "success")
                self.go("/dashboard")
            else:
                self.show_snackbar("保存失败", "error")

        except ValueError:
            self.show_snackbar("请输入有效的金额", "error")
        except Exception as ex:
            self.show_snackbar(f"保存失败: {ex}", "error")

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
