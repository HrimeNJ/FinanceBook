"""
RecordsView for ui
"""

from datetime import datetime, timedelta
from typing import List

import flet as ft

from components.sidebar import Sidebar
from models.record import Record


class RecordsView(ft.View):
    """记录列表视图"""

    def __init__(self, state, go):
        super().__init__(route="/records")
        self.state = state
        self.go = go
        self.page = state.page

        # 初始化过滤器
        self.current_filter = "all"
        self.current_period = "all"
        self.search_text = ""

        # 筛选组件引用
        self.search_field = None
        self.filter_dropdown = None
        self.date_filter = None

        self.controls = [self.create_records_layout()]

    def create_records_layout(self):
        """创建记录布局"""
        # 侧边栏
        sidebar = Sidebar(
            self.page, self.state.current_user, self.handle_logout, self.go
        ).create_sidebar()

        # 搜索和筛选组件
        self.search_field = ft.TextField(
            label="搜索交易记录...",
            width=300,
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.on_search_change,
        )

        self.filter_dropdown = ft.Dropdown(
            label="筛选",
            width=150,
            options=[
                ft.dropdown.Option("all", "全部"),
                ft.dropdown.Option("income", "收入"),
                ft.dropdown.Option("expense", "支出"),
            ],
            value="all",
            on_change=self.on_filter_change,
        )

        self.date_filter = ft.Dropdown(
            label="时间段",
            width=150,
            options=[
                ft.dropdown.Option("today", "今天"),
                ft.dropdown.Option("week", "本周"),
                ft.dropdown.Option("month", "本月"),
                ft.dropdown.Option("year", "本年"),
                ft.dropdown.Option("all", "全部"),
            ],
            value="all",
            on_change=self.on_date_change,
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
                    # 页面标题 - 固定在顶部
                    self.create_page_header("交易记录"),
                    # 可滚动的内容区域
                    ft.Container(
                        content=ft.Column(
                            [
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
                                            ft.ResponsiveRow(
                                                [
                                                    ft.Container(
                                                        content=self.search_field,
                                                        col={"sm": 12, "md": 6},
                                                    ),
                                                    ft.Container(
                                                        content=self.filter_dropdown,
                                                        col={"sm": 6, "md": 3},
                                                    ),
                                                    ft.Container(
                                                        content=self.date_filter,
                                                        col={"sm": 6, "md": 3},
                                                    ),
                                                ],
                                                spacing=16,
                                            ),
                                        ]
                                    ),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.all(20),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                    border=ft.border.all(1, ft.Colors.GREY_200),
                                ),
                                # 记录列表
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text(
                                                        "交易记录",
                                                        size=16,
                                                        weight=ft.FontWeight.W_600,
                                                    ),
                                                    ft.Text(
                                                        f"{len(self.get_filtered_records())} 条记录",
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
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                    border=ft.border.all(1, ft.Colors.GREY_200),
                                ),
                                # 底部留白
                                ft.Container(height=50),
                            ],
                            spacing=0,
                            scroll=ft.ScrollMode.AUTO,
                        ),
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
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
        )

    def get_user_records(self) -> List[Record]:
        """获取用户记录"""
        if self.state.current_user:
            return self.state.records.copy()
        return []

    def get_filtered_records(self) -> List[Record]:
        """获取筛选后的记录"""
        all_records = self.get_user_records()
        if not all_records:
            return []

        filtered_records = all_records.copy()

        # 1. 按记录类型筛选
        if self.current_filter != "all":
            filtered_records = [
                record
                for record in filtered_records
                if record.record_type == self.current_filter
            ]

        # 2. 按时间段筛选
        if self.current_period != "all":
            date_range = self.get_date_range(self.current_period)
            if date_range:
                start_date, end_date = date_range
                filtered_records = [
                    record
                    for record in filtered_records
                    if start_date <= record.date.date() <= end_date
                ]

        # 3. 按搜索关键词筛选
        if self.search_text.strip():
            search_lower = self.search_text.lower().strip()
            res = []

            for record in filtered_records:
                # 获取分类名称
                category = self.state.get_category_by_id(record.category_id)
                category_name = category.name if category else ""

                # 搜索条件：金额、备注、分类名称
                if (
                    search_lower in str(record.amount)
                    or search_lower in record.note.lower()
                    or search_lower in category_name.lower()
                ):
                    res.append(record)

            filtered_records = res

        # 按日期降序排序
        filtered_records.sort(key=lambda x: x.date, reverse=True)
        return filtered_records

    def get_date_range(self, period: str):
        """获取日期范围"""
        today = datetime.now().date()

        if period == "today":
            return today, today
        elif period == "week":
            start_of_week = today - timedelta(days=today.weekday())
            return start_of_week, today
        elif period == "month":
            start_of_month = today.replace(day=1)
            return start_of_month, today
        elif period == "year":
            start_of_year = today.replace(month=1, day=1)
            return start_of_year, today

        return None

    def load_records(self):
        """加载记录列表"""
        filtered_records = self.get_filtered_records()

        self.records_list.controls.clear()

        if not filtered_records:
            # 显示无记录消息
            empty_message = self.get_empty_message()
            self.records_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.RECEIPT_LONG, size=64, color=ft.Colors.GREY_400
                            ),
                            ft.Text(
                                empty_message,
                                size=16,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                    ),
                    alignment=ft.alignment.center,
                    height=200,
                )
            )
        else:
            # 显示记录卡片
            for record in filtered_records:
                record_card = self.create_record_card(record)
                self.records_list.controls.append(record_card)

        if self.page:
            self.page.update()

    def get_empty_message(self) -> str:
        """根据当前筛选条件返回相应的空数据提示"""
        if self.search_text.strip():
            return f"未找到包含 '{self.search_text}' 的记录"
        elif self.current_filter != "all" and self.current_period != "all":
            filter_text = "收入" if self.current_filter == "income" else "支出"
            period_text = {
                "today": "今天",
                "week": "本周",
                "month": "本月",
                "year": "本年",
            }.get(self.current_period, "")
            return f"暂无{period_text}{filter_text}记录"
        elif self.current_filter != "all":
            filter_text = "收入" if self.current_filter == "income" else "支出"
            return f"暂无{filter_text}记录"
        elif self.current_period != "all":
            period_text = {
                "today": "今天",
                "week": "本周",
                "month": "本月",
                "year": "本年",
            }.get(self.current_period, "")
            return f"暂无{period_text}记录"
        else:
            return "暂无记录，点击右上角添加第一笔记录吧！"

    def create_record_card(self, record: Record) -> ft.Container:
        """创建记录卡片"""
        category = self.state.get_category_by_id(record.category_id)
        category_name = category.name if category else "未知分类"

        # 格式化日期显示
        date_str = record.date.strftime("%m/%d")
        if record.date.date() == datetime.now().date():
            date_str = "今天"
        elif record.date.date() == datetime.now().date() - timedelta(days=1):
            date_str = "昨天"

        return ft.Container(
            content=ft.Row(
                [
                    # 收入/支出图标
                    ft.Container(
                        content=ft.Icon(
                            (
                                ft.Icons.ARROW_UPWARD
                                if record.record_type == "income"
                                else ft.Icons.ARROW_DOWNWARD
                            ),
                            color=(
                                ft.Colors.GREEN_600
                                if record.record_type == "income"
                                else ft.Colors.RED_600
                            ),
                            size=20,
                        ),
                        width=40,
                        height=40,
                        bgcolor=(
                            ft.Colors.GREEN_50
                            if record.record_type == "income"
                            else ft.Colors.RED_50
                        ),
                        border_radius=20,
                        alignment=ft.alignment.center,
                    ),
                    # 金额和分类信息
                    ft.Column(
                        [
                            ft.Text(
                                f"¥{record.amount:.2f}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_900,
                            ),
                            ft.Text(
                                f"{category_name}",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    # 备注信息（如果有）
                    (
                        ft.Container(
                            content=ft.Text(
                                (
                                    record.note[:20] + "..."
                                    if len(record.note) > 20
                                    else record.note
                                ),
                                size=12,
                                color=ft.Colors.GREY_500,
                                max_lines=1,
                            ),
                            width=120,
                            visible=bool(record.note.strip()),
                        )
                        if record.note.strip()
                        else ft.Container(width=120)
                    ),
                    # 日期
                    ft.Text(
                        date_str,
                        size=12,
                        color=ft.Colors.GREY_600,
                        width=50,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    # 操作按钮
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=ft.Colors.BLUE_400,
                                icon_size=18,
                                tooltip="编辑",
                                on_click=lambda e, record_id=record.record_id: self.edit_record(
                                    record_id
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_400,
                                icon_size=18,
                                tooltip="删除",
                                on_click=lambda e, record_id=record.record_id: self.confirm_delete_record(
                                    record_id
                                ),
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=12,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=ft.padding.all(16),
            margin=ft.margin.symmetric(vertical=2),
            border=ft.border.all(1, ft.Colors.GREY_100),
            on_hover=self.on_record_hover,
        )

    def on_record_hover(self, e):
        """记录卡片悬停效果"""
        if e.data == "true":  # 鼠标进入
            e.control.border = ft.border.all(1, ft.Colors.BLUE_200)
            e.control.bgcolor = ft.Colors.BLUE_50
        else:  # 鼠标离开
            e.control.border = ft.border.all(1, ft.Colors.GREY_100)
            e.control.bgcolor = ft.Colors.WHITE
        e.control.update()

    # 事件处理方法
    def on_search_change(self, e):
        """搜索文本变化"""
        self.search_text = e.control.value
        self.load_records()

    def on_filter_change(self, e):
        """筛选类型变化"""
        self.current_filter = e.control.value
        self.load_records()

    def on_date_change(self, e):
        """时间段变化"""
        self.current_period = e.control.value
        self.load_records()

    def edit_record(self, record_id):
        """编辑记录"""
        # TODO: 跳转到编辑页面，传递记录ID
        self.show_snackbar("编辑功能开发中")
        return
        self.go(f"/add_record?edit={record_id}")

    def confirm_delete_record(self, record_id):
        """确认删除记录"""

        def close_dialog(e):
            dialog.open = False
            self.page.update()

        def delete_confirmed(e):
            if self.state.delete_record(record_id):
                self.show_snackbar("记录删除成功", "success")
                self.load_records()
            else:
                self.show_snackbar("删除失败", "error")
            close_dialog(e)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("确认删除"),
            content=ft.Text("确定要删除这条记录吗？此操作无法撤销。"),
            actions=[
                ft.TextButton("取消", on_click=close_dialog),
                ft.TextButton(
                    "删除",
                    on_click=delete_confirmed,
                    style=ft.ButtonStyle(color=ft.Colors.RED),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def delete_record(self, record_id):
        """删除记录（直接删除，不推荐）"""
        if self.state.delete_record(record_id):
            self.show_snackbar("记录删除成功", "success")
            self.load_records()
        else:
            self.show_snackbar("删除失败", "error")

    def export_records(self, e):
        """导出记录"""
        filtered_records = self.get_filtered_records()
        if not filtered_records:
            self.show_snackbar("没有可导出的记录", "info")
            return

        # TODO: 实现实际的导出功能
        self.show_snackbar(
            f"导出功能开发中，当前有 {len(filtered_records)} 条记录", "info"
        )

    def handle_logout(self, e):
        """处理登出"""
        self.state.clear_user_data()
        self.go("/welcome")

    def show_snackbar(self, message: str, message_type: str = "info"):
        """显示提示消息"""
        colors = {
            "success": ft.Colors.GREEN,
            "error": ft.Colors.RED,
            "info": ft.Colors.BLUE,
        }

        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=colors.get(message_type, ft.Colors.BLUE),
            show_close_icon=True,
        )

        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()
