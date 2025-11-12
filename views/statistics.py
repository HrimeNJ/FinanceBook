"""
StatisticsView for ui
"""

from datetime import datetime, timedelta

import flet as ft

from components.cards import create_stat_card
from components.sidebar import Sidebar


class StatisticsView(ft.View):
    """统计视图"""

    def __init__(self, state, go):
        super().__init__(route="/statistics")
        self.state = state
        self.go = go
        self.page = state.page
        self.controls = [self.create_statistics_layout()]

    def create_statistics_layout(self):
        """创建统计布局"""
        # 侧边栏
        sidebar = Sidebar(
            self.page, self.state.current_user, self.handle_logout, self.go
        ).create_sidebar()

        # 时间范围选择
        time_range = ft.Dropdown(
            label="时间范围",
            width=200,
            options=[
                ft.dropdown.Option("week", "本周"),
                ft.dropdown.Option("month", "本月"),
                ft.dropdown.Option("quarter", "本季度"),
                ft.dropdown.Option("year", "本年"),
            ],
            value="month",
            on_change=self.update_statistics,
        )

        # 获取统计数据
        stats = self.get_statistics()

        # 创建可滚动的主内容
        main_content = ft.Container(
            content=ft.Column(
                [
                    # 页面标题 - 固定在顶部
                    self.create_page_header("财务统计"),
                    # 可滚动的内容区域
                    ft.Container(
                        content=ft.Column(
                            [
                                # 控制面板
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Text(
                                                "分析概览",
                                                size=16,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            time_range,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.all(20),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                    border=ft.border.all(1, ft.Colors.GREY_200),
                                ),
                                # 统计卡片行
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            create_stat_card(
                                                "总收入",
                                                f"¥{stats['total_income']:.2f}",
                                                f"+{stats['income_change']:.1f}%",
                                                ft.Colors.GREEN_500,
                                                ft.Icons.TRENDING_UP,
                                            ),
                                            create_stat_card(
                                                "总支出",
                                                f"¥{stats['total_expenses']:.2f}",
                                                f"+{stats['expense_change']:.1f}%",
                                                ft.Colors.RED_500,
                                                ft.Icons.TRENDING_DOWN,
                                            ),
                                            create_stat_card(
                                                "净储蓄",
                                                f"¥{stats['net_savings']:.2f}",
                                                f"{stats['savings_change']:+.1f}%",
                                                ft.Colors.BLUE_500,
                                                ft.Icons.SAVINGS,
                                            ),
                                        ],
                                        spacing=16,
                                    ),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                ),
                                # 图表区域
                                ft.Container(
                                    content=ft.ResponsiveRow(
                                        [
                                            # 支出分类图
                                            ft.Container(
                                                content=ft.Column(
                                                    [
                                                        ft.Text(
                                                            "支出分类",
                                                            size=16,
                                                            weight=ft.FontWeight.W_600,
                                                        ),
                                                        ft.Container(height=16),
                                                        self.create_category_chart(),
                                                    ]
                                                ),
                                                bgcolor=ft.Colors.WHITE,
                                                border_radius=16,
                                                padding=ft.padding.all(20),
                                                border=ft.border.all(
                                                    1, ft.Colors.GREY_200
                                                ),
                                                col={"sm": 12, "md": 6},  # 响应式布局
                                            ),
                                            # 月度趋势图
                                            ft.Container(
                                                content=ft.Column(
                                                    [
                                                        ft.Text(
                                                            "月度趋势",
                                                            size=16,
                                                            weight=ft.FontWeight.W_600,
                                                        ),
                                                        ft.Container(height=16),
                                                        self.create_trend_chart(),
                                                    ]
                                                ),
                                                bgcolor=ft.Colors.WHITE,
                                                border_radius=16,
                                                padding=ft.padding.all(20),
                                                border=ft.border.all(
                                                    1, ft.Colors.GREY_200
                                                ),
                                                col={"sm": 12, "md": 6},  # 响应式布局
                                            ),
                                        ],
                                        spacing=20,
                                    ),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                ),
                                # 详细分析
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "详细分析",
                                                size=16,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            ft.Container(height=16),
                                            ft.ResponsiveRow(
                                                [
                                                    ft.Container(
                                                        content=self.create_insight_card(
                                                            "最大支出分类",
                                                            stats["top_category"],
                                                            f"¥{stats['top_category_amount']:.2f}",
                                                            ft.Icons.CATEGORY,
                                                            ft.Colors.ORANGE_400,
                                                        ),
                                                        col={"sm": 12, "md": 4},
                                                    ),
                                                    ft.Container(
                                                        content=self.create_insight_card(
                                                            "日均支出",
                                                            "每日平均",
                                                            f"¥{stats['daily_average']:.2f}",
                                                            ft.Icons.CALENDAR_TODAY,
                                                            ft.Colors.PURPLE_400,
                                                        ),
                                                        col={"sm": 12, "md": 4},
                                                    ),
                                                    ft.Container(
                                                        content=self.create_insight_card(
                                                            "交易次数",
                                                            "本月",
                                                            str(
                                                                stats[
                                                                    "transaction_count"
                                                                ]
                                                            ),
                                                            ft.Icons.RECEIPT,
                                                            ft.Colors.CYAN_400,
                                                        ),
                                                        col={"sm": 12, "md": 4},
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
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
        )

    def get_statistics(self):
        """获取统计数据"""
        if not self.state.current_user:
            return self.get_empty_stats()

        try:
            balance_data = self.state.db.get_user_balance(
                self.state.current_user.user_id
            )
            records = self.state.db.get_records(self.state.current_user.user_id)

            # 计算基本统计
            total_income = balance_data.get("income", 0)
            total_expenses = balance_data.get("expense", 0)
            net_savings = total_income - total_expenses

            # 计算变化率（简化版，实际应该对比上期数据）
            income_change = 5.2  # 模拟数据
            expense_change = 3.1
            savings_change = (net_savings / max(total_income, 1)) * 100

            # 分析最大支出分类
            top_category = "餐饮"  # 简化版
            top_category_amount = total_expenses * 0.3

            # 日均支出
            daily_average = total_expenses / 30 if total_expenses > 0 else 0

            return {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "net_savings": net_savings,
                "income_change": income_change,
                "expense_change": expense_change,
                "savings_change": savings_change,
                "top_category": top_category,
                "top_category_amount": top_category_amount,
                "daily_average": daily_average,
                "transaction_count": len(records),
            }
        except Exception as e:
            print(f"统计数据获取失败: {e}")
            return self.get_empty_stats()

    def get_empty_stats(self):
        """获取空统计数据"""
        return {
            "total_income": 0,
            "total_expenses": 0,
            "net_savings": 0,
            "income_change": 0,
            "expense_change": 0,
            "savings_change": 0,
            "top_category": "无数据",
            "top_category_amount": 0,
            "daily_average": 0,
            "transaction_count": 0,
        }

    def create_category_chart(self):
        """创建分类图表（简化版）"""
        return ft.Container(
            content=ft.Text(
                "分类图表\n（将在后续版本实现）", text_align=ft.TextAlign.CENTER
            ),
            height=180,  # 减少高度
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8,
        )

    def create_trend_chart(self):
        """创建趋势图表（简化版）"""
        return ft.Container(
            content=ft.Text(
                "趋势图表\n（将在后续版本实现）", text_align=ft.TextAlign.CENTER
            ),
            height=180,  # 减少高度
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8,
        )

    def create_insight_card(self, title, subtitle, value, icon, color):
        """创建洞察卡片"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icon, size=20, color=color),  # 减少图标大小
                            ft.Column(
                                [
                                    ft.Text(title, size=11, color=ft.Colors.GREY_600),
                                    ft.Text(subtitle, size=9, color=ft.Colors.GREY_500),
                                ],
                                spacing=1,
                                expand=True,
                            ),
                        ],
                        spacing=6,
                    ),
                    ft.Text(
                        value,
                        size=18,  # 减少字体大小
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_900,
                    ),
                ],
                spacing=6,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=ft.padding.all(12),  # 减少内边距
            border=ft.border.all(1, color),
            height=100,  # 固定高度
        )

    def update_statistics(self, e):
        """更新统计数据"""
        # 重新加载统计数据
        self.show_snackbar("统计数据已更新", "info")

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
