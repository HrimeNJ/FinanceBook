"""
RecordsView for ui
"""

import flet as ft

from components.sidebar import Sidebar


class RecordsView(ft.View):
    """记录列表视图"""

    def __init__(self, state, go):
        super().__init__(route="/records")
        self.state = state
        self.go = go
        self.page = state.page

        # 初始化过滤器
        self.current_filter = "all"
        self.current_period = "month"
        self.search_text = ""

        self.controls = [self.create_records_layout()]

    def create_records_layout(self):
        """创建记录布局"""
        # 侧边栏
        sidebar = Sidebar(
            self.page, self.state.current_user, self.handle_logout, self.go
        ).create_sidebar()

        # 搜索和筛选组件
        search_field = ft.TextField(
            label="搜索交易记录...",
            width=300,
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.filter_records,
        )

        filter_dropdown = ft.Dropdown(
            label="筛选",
            width=150,
            options=[
                ft.dropdown.Option("all", "全部"),
                ft.dropdown.Option("income", "收入"),
                ft.dropdown.Option("expense", "支出"),
            ],
            value="all",
            on_change=self.filter_records,
        )

        date_filter = ft.Dropdown(
            label="时间段",
            width=150,
            options=[
                ft.dropdown.Option("today", "今天"),
                ft.dropdown.Option("week", "本周"),
                ft.dropdown.Option("month", "本月"),
                ft.dropdown.Option("year", "本年"),
                ft.dropdown.Option("all", "全部"),
            ],
            value="month",
            on_change=self.filter_records,
        )

        # 记录列表
        self.records_list = ft.Column(
            [], spacing=8, expand=True, scroll=ft.ScrollMode.AUTO
        )

        # 加载记录
        self.load_records()

        # 主内容
        main_content = ft.Container(
            content=ft.Column(
                [
                    self.create_page_header("交易记录"),
                    # 筛选栏
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(
                                            "筛选器",
                                            size=16,
                                            weight=ft.FontWeight.W_600,
                                        ),
                                        ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    text="导出",
                                                    icon=ft.Icons.DOWNLOAD,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ft.Colors.GREEN_600,
                                                        color=ft.Colors.WHITE,
                                                        shape=ft.RoundedRectangleBorder(
                                                            radius=8
                                                        ),
                                                    ),
                                                    on_click=self.export_records,
                                                ),
                                                ft.ElevatedButton(
                                                    text="添加新记录",
                                                    icon=ft.Icons.ADD,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ft.Colors.BLUE_600,
                                                        color=ft.Colors.WHITE,
                                                        shape=ft.RoundedRectangleBorder(
                                                            radius=8
                                                        ),
                                                    ),
                                                    on_click=lambda e: self.go(
                                                        "/add_record"
                                                    ),
                                                ),
                                            ],
                                            spacing=12,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Container(height=16),
                                ft.Row(
                                    [search_field, filter_dropdown, date_filter],
                                    spacing=16,
                                ),
                            ]
                        ),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=16,
                        padding=ft.padding.all(20),
                        margin=ft.margin.all(20),
                        border=ft.border.all(1, ft.Colors.GREY_200),
                    ),
                    # 记录列表
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(
                                            "最近交易",
                                            size=16,
                                            weight=ft.FontWeight.W_600,
                                        ),
                                        ft.Text(
                                            f"{len(self.get_user_records())} 条记录",
                                            size=14,
                                            color=ft.Colors.GREY_600,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Container(height=16),
                                self.records_list,
                            ]
                        ),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=16,
                        padding=ft.padding.all(20),
                        margin=ft.margin.symmetric(horizontal=20),
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        expand=True,
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

    def get_user_records(self):
        """获取用户记录"""
        if self.state.current_user:
            return self.state.db.get_records(self.state.current_user.user_id)
        return []

    def load_records(self):
        """加载记录列表"""
        records = self.get_user_records()
        self.records_list.controls.clear()

        if not records:
            self.records_list.controls.append(
                ft.Container(
                    content=ft.Text("暂无记录", text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    height=200,
                )
            )
        else:
            for record in records:
                category = self.state.db.get_category(record.category_id)
                category_name = category.name if category else "未知分类"

                record_card = ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                (
                                    ft.Icons.ARROW_UPWARD
                                    if record.record_type == "income"
                                    else ft.Icons.ARROW_DOWNWARD
                                ),
                                color=(
                                    ft.Colors.GREEN
                                    if record.record_type == "income"
                                    else ft.Colors.RED
                                ),
                                size=24,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        f"¥{record.amount:.2f}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        f"{category_name} - {record.note}",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                record.date.strftime("%Y-%m-%d"),
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_400,
                                tooltip="删除",
                                on_click=lambda e, record_id=record.record_id: self.delete_record(
                                    record_id
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=8,
                    padding=ft.padding.all(12),
                    margin=ft.margin.symmetric(vertical=2),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                )
                self.records_list.controls.append(record_card)

        self.page.update()

    def filter_records(self, e):
        """过滤记录"""
        # 这里可以实现更复杂的过滤逻辑
        self.load_records()

    def delete_record(self, record_id):
        """删除记录"""
        if self.state.delete_record(record_id):
            self.show_snackbar("记录删除成功", "success")
            self.load_records()
        else:
            self.show_snackbar("删除失败", "error")

    def export_records(self, e):
        """导出记录"""
        self.show_snackbar("导出功能将在后续版本中实现", "info")

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
