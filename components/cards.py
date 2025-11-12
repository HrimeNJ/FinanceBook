"""
Card components for the application
"""

import flet as ft


def create_stat_card(title, value, change, color, icon):
    """创建统计卡片"""
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    title,
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    weight=ft.FontWeight.W_500,
                                ),
                                ft.Text(
                                    value,
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_900,
                                ),
                                ft.Text(
                                    f"{change} 较上月",
                                    size=12,
                                    color=color,
                                ),
                            ],
                            expand=True,
                            spacing=4,
                        ),
                        ft.Container(
                            content=ft.Icon(icon, size=32, color=color),
                            bgcolor=ft.Colors.with_opacity(0.1, color),
                            border_radius=12,
                            padding=ft.padding.all(8),
                        ),
                    ]
                )
            ]
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        padding=ft.padding.all(20),
        border=ft.border.all(1, ft.Colors.GREY_200),
        expand=True,
    )


def create_page_header(title, subtitle=""):
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
                    ft.Text(
                        subtitle,
                        size=16,
                        color=ft.Colors.GREY_600,
                    )
                    if subtitle
                    else ft.Container()
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=30, vertical=30),
    )


import flet as ft


class RecentTransactionsList(ft.Column):
    """最近交易列表组件"""

    def __init__(self, records, state):
        super().__init__()
        self.records = records
        self.state = state
        self.spacing = 0
        self.controls = self._build_items()

    def _build_items(self):
        if not self.records:
            return [
                ft.Container(
                    content=ft.Text("暂无交易记录", text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    height=100,
                )
            ]

        items = []
        for record in self.records:
            category = self.state.get_category_by_id(record.category_id)
            category_name = category.name if category else "未知分类"

            item = ft.ListTile(
                leading=ft.Icon(
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
                ),
                title=ft.Text(record.note or category_name),
                subtitle=ft.Text(
                    f"{category_name} • {record.date.strftime('%Y-%m-%d')}"
                ),
                trailing=ft.Text(
                    f"{'+' if record.record_type == 'income' else '-'}¥{record.amount:.2f}",
                    color=(
                        ft.Colors.GREEN
                        if record.record_type == "income"
                        else ft.Colors.RED
                    ),
                    weight=ft.FontWeight.BOLD,
                ),
            )
            items.append(item)
        return items


class StatCard(ft.Container):
    """统计卡片组件"""

    def __init__(self, title, value, change, color, icon):
        super().__init__()
        self.content = create_stat_card(title, value, change, color, icon)
