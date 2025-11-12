"""
StatisticsView for ui
"""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

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
        self.current_period = "month"
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
            # 获取当前周期和上一周期的日期范围
            current_range = self.get_period_date_range()
            previous_range = self.get_previous_period_date_range()

            if not current_range:
                return self.get_empty_stats()

            current_start, current_end = current_range
            records = self.state.records.copy()

            # 当前周期统计
            current_income = 0
            current_expense = 0
            current_records = []
            category_expenses = defaultdict(float)

            for record in records:
                record_date = record.date.date()
                if current_start <= record_date <= current_end:
                    current_records.append(record)
                    if record.record_type == "income":
                        current_income += record.amount
                    elif record.record_type == "expense":
                        current_expense += record.amount
                        category = self.state.get_category_by_id(record.category_id)
                        category_name = category.name if category else "其他"
                        category_expenses[category_name] += record.amount

            # 上一周期统计（用于计算变化率）
            previous_income = 0
            previous_expense = 0

            if previous_range:
                previous_start, previous_end = previous_range
                for record in records:
                    record_date = record.date.date()
                    if previous_start <= record_date <= previous_end:
                        if record.record_type == "income":
                            previous_income += record.amount
                        elif record.record_type == "expense":
                            previous_expense += record.amount

            # 计算变化率
            income_change = self.calculate_change_rate(current_income, previous_income)
            expense_change = self.calculate_change_rate(
                current_expense, previous_expense
            )

            # 计算净储蓄
            net_savings = current_income - current_expense
            previous_savings = previous_income - previous_expense
            savings_change = self.calculate_change_rate(net_savings, previous_savings)

            # 找出最大支出分类
            top_category = "暂无数据"
            top_category_amount = 0
            if category_expenses:
                top_category = max(category_expenses.items(), key=lambda x: x[1])
                top_category_amount = top_category[1]
                top_category = top_category[0]

            # 计算日均支出
            days_in_period = (current_end - current_start).days + 1
            daily_average = (
                current_expense / days_in_period if days_in_period > 0 else 0
            )

            return {
                "total_income": current_income,
                "total_expenses": current_expense,
                "net_savings": net_savings,
                "income_change": income_change,
                "expense_change": expense_change,
                "savings_change": savings_change,
                "top_category": top_category,
                "top_category_amount": top_category_amount,
                "daily_average": daily_average,
                "transaction_count": len(current_records),
            }
        except Exception as e:
            print(f"统计数据获取失败: {e}")
            import traceback

            traceback.print_exc()
            return self.get_empty_stats()

    def calculate_change_rate(self, current: float, previous: float) -> float:
        """计算变化率（百分比）"""
        if previous == 0:
            if current > 0:
                return 100.0  # 从0增长到有值，显示100%增长
            return 0.0

        change_rate = ((current - previous) / previous) * 100
        return round(change_rate, 1)

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
        """创建支出分类饼图"""
        category_data = self.get_category_data()

        if not category_data:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.PIE_CHART_OUTLINE,
                            size=48,
                            color=ft.Colors.GREY_400,
                        ),
                        ft.Text("暂无数据", size=14, color=ft.Colors.GREY_500),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                height=250,
                alignment=ft.alignment.center,
            )

        # 计算总金额
        total_amount = sum(category_data.values())

        # 创建分类列表
        category_items = []
        pie_sections = []

        for index, (category_name, amount) in enumerate(category_data.items()):
            percentage = (amount / total_amount * 100) if total_amount > 0 else 0
            color = self.get_category_color(index)

            # 分类列表项
            category_items.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                width=12,
                                height=12,
                                bgcolor=color,
                                border_radius=2,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        category_name,
                                        size=12,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                    ft.Text(
                                        f"¥{amount:.2f}",
                                        size=11,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                f"{percentage:.1f}%",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=color,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(vertical=6),
                )
            )

            # 饼图扇区
            pie_sections.append(
                ft.PieChartSection(
                    value=amount,
                    title=f"{percentage:.1f}%",
                    color=color,
                    radius=50,
                    title_style=ft.TextStyle(
                        size=10,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                )
            )

        # 创建饼图
        pie_chart = ft.PieChart(
            sections=pie_sections,
            sections_space=2,
            center_space_radius=40,
            expand=False,
            width=150,
            height=150,
        )

        # 饼图容器,显示总金额在中心
        pie_visual = ft.Container(
            content=ft.Stack(
                [
                    pie_chart,
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "总支出",
                                    size=10,
                                    color=ft.Colors.GREY_600,
                                ),
                                ft.Text(
                                    f"¥{total_amount:.0f}",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        width=150,
                        height=150,
                        alignment=ft.alignment.center,
                    ),
                ],
            ),
            margin=ft.margin.only(bottom=16, right=20),
        )

        return ft.Container(
            content=ft.Row(
                [
                    pie_visual,
                    ft.Container(
                        content=ft.Column(
                            category_items,
                            spacing=4,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        expand=True,
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            height=250,
        )

    def create_trend_chart(self):
        """创建最近7天收支趋势折线图"""
        trend_data = self.get_trend_data()

        if not trend_data["dates"]:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.SHOW_CHART, size=48, color=ft.Colors.GREY_400),
                        ft.Text("暂无数据", size=14, color=ft.Colors.GREY_500),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                height=250,
                alignment=ft.alignment.center,
            )

        income_data = trend_data["income"]
        expense_data = trend_data["expense"]
        date_labels = trend_data["date_labels"]

        # 计算最大值用于缩放
        max_value = max(
            max(income_data) if income_data else 0,
            max(expense_data) if expense_data else 0,
        )
        max_value = max_value * 1.2 if max_value > 0 else 100  # 留20%空间

        # 创建折线图
        income_spots = []
        expense_spots = []

        for i, (income, expense) in enumerate(zip(income_data, expense_data)):
            income_spots.append(ft.LineChartDataPoint(i, income))
            expense_spots.append(ft.LineChartDataPoint(i, expense))

        # 创建折线图
        line_chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=income_spots,
                    stroke_width=3,
                    color=ft.Colors.GREEN_500,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_500),
                ),
                ft.LineChartData(
                    data_points=expense_spots,
                    stroke_width=3,
                    color=ft.Colors.RED_500,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_500),
                ),
            ],
            border=ft.Border(
                bottom=ft.BorderSide(1, ft.Colors.GREY_300),
                left=ft.BorderSide(1, ft.Colors.GREY_300),
            ),
            left_axis=ft.ChartAxis(
                labels_size=50,
                title=ft.Text("金额"),
                title_size=20,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Text(label, size=10, color=ft.Colors.GREY_600),
                    )
                    for i, label in enumerate(date_labels)
                ],
                labels_size=30,
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.GREY_900),
            min_y=0,
            max_y=max_value,
            min_x=0,
            max_x=len(date_labels) - 1,
            expand=True,
        )

        # 图例
        legend = ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            width=16,
                            height=3,
                            bgcolor=ft.Colors.GREEN_500,
                            border_radius=1,
                        ),
                        ft.Text("收入", size=11, color=ft.Colors.GREY_600),
                    ],
                    spacing=6,
                ),
                ft.Row(
                    [
                        ft.Container(
                            width=16,
                            height=3,
                            bgcolor=ft.Colors.RED_500,
                            border_radius=1,
                        ),
                        ft.Text("支出", size=11, color=ft.Colors.GREY_600),
                    ],
                    spacing=6,
                ),
            ],
            spacing=16,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=line_chart,
                        height=180,
                        padding=ft.padding.only(right=10, top=10),
                    ),
                    ft.Container(height=10),
                    legend,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            height=250,
        )

    def get_category_data(self) -> Dict[str, float]:
        """获取分类统计数据（仅支出）"""
        if not self.state.current_user:
            return {}

        # 获取当前时间段的记录
        records = self.get_period_records()

        # 按分类统计支出
        category_totals = defaultdict(float)

        for record in records:
            if record.record_type == "expense":
                category = self.state.get_category_by_id(record.category_id)
                category_name = category.name if category else "其他"
                category_totals[category_name] += record.amount

        # 按金额排序，取前6个分类
        sorted_categories = category_totals
        if len(category_totals) > 6:
            sorted_categories = dict(
                sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:6]
            )

        return sorted_categories

    def get_trend_data(self) -> Dict[str, List]:
        """获取最近7天的趋势数据"""
        if not self.state.current_user:
            return {"dates": [], "income": [], "expense": [], "date_labels": []}

        # 获取最近7天的日期范围
        today = datetime.now().date()
        start_date = today - timedelta(days=6)  # 包括今天共7天

        # 生成7天的日期列表
        date_list = []
        for i in range(7):
            date_list.append(start_date + timedelta(days=i))

        # 获取所有记录
        records = self.state.records.copy()

        # 按日期统计收入和支出
        income_data = []
        expense_data = []
        date_labels = []

        for date in date_list:
            daily_income = 0
            daily_expense = 0

            # 统计当天的收入和支出
            for record in records:
                if record.date.date() == date:
                    if record.record_type == "income":
                        daily_income += record.amount
                    elif record.record_type == "expense":
                        daily_expense += record.amount

            income_data.append(daily_income)
            expense_data.append(daily_expense)

            # 生成日期标签 (月/日格式)
            date_labels.append(date.strftime("%m/%d"))

        return {
            "dates": date_list,
            "income": income_data,
            "expense": expense_data,
            "date_labels": date_labels,
        }

    def get_period_records(self):
        """获取当前时间段的记录"""
        if not self.state.current_user:
            return []

        all_records = self.state.records.copy()
        date_range = self.get_period_date_range()

        if not date_range:
            return all_records

        start_date, end_date = date_range

        return [
            record
            for record in all_records
            if start_date <= record.date.date() <= end_date
        ]

    def get_period_date_range(self) -> Tuple[datetime.date, datetime.date]:
        """根据当前时间段获取日期范围"""
        today = datetime.now().date()

        if self.current_period == "week":
            start_of_week = today - timedelta(days=today.weekday())
            return start_of_week, today
        elif self.current_period == "month":
            start_of_month = today.replace(day=1)
            return start_of_month, today
        elif self.current_period == "quarter":
            # 当前季度
            current_quarter = (today.month - 1) // 3
            start_month = current_quarter * 3 + 1
            start_of_quarter = today.replace(month=start_month, day=1)
            return start_of_quarter, today
        elif self.current_period == "year":
            start_of_year = today.replace(month=1, day=1)
            return start_of_year, today

        return None

    def get_previous_period_date_range(self) -> Tuple[datetime.date, datetime.date]:
        """获取上一周期的日期范围"""
        today = datetime.now().date()

        if self.current_period == "week":
            # 上周
            start_of_week = today - timedelta(days=today.weekday())
            previous_start = start_of_week - timedelta(days=7)
            previous_end = start_of_week - timedelta(days=1)
            return previous_start, previous_end

        elif self.current_period == "month":
            # 上月
            first_day_current = today.replace(day=1)
            last_day_previous = first_day_current - timedelta(days=1)
            first_day_previous = last_day_previous.replace(day=1)
            return first_day_previous, last_day_previous

        elif self.current_period == "quarter":
            # 上季度
            current_quarter = (today.month - 1) // 3

            if current_quarter == 0:
                # 如果当前是第一季度，上一季度是去年第四季度
                previous_year = today.year - 1
                previous_start = datetime(previous_year, 10, 1).date()
                previous_end = datetime(previous_year, 12, 31).date()
            else:
                previous_quarter = current_quarter - 1
                previous_start_month = previous_quarter * 3 + 1
                previous_start = today.replace(month=previous_start_month, day=1)

                # 上季度最后一天
                current_start_month = current_quarter * 3 + 1
                current_start = today.replace(month=current_start_month, day=1)
                previous_end = current_start - timedelta(days=1)

            return previous_start, previous_end

        elif self.current_period == "year":
            # 去年
            previous_year = today.year - 1
            previous_start = datetime(previous_year, 1, 1).date()
            previous_end = datetime(previous_year, 12, 31).date()
            return previous_start, previous_end

        return None

    def get_category_color(self, index: int) -> str:
        """获取分类颜色"""
        colors = [
            ft.Colors.BLUE_400,
            ft.Colors.GREEN_400,
            ft.Colors.ORANGE_400,
            ft.Colors.RED_400,
            ft.Colors.PURPLE_400,
            ft.Colors.CYAN_400,
            ft.Colors.PINK_400,
            ft.Colors.INDIGO_400,
        ]
        return colors[index % len(colors)]

    def update_statistics(self, e):
        """更新统计数据"""
        # 更新当前时间段
        self.current_period = e.control.value

        # 重新创建整个布局以更新图表
        self.controls = [self.create_statistics_layout()]
        self.page.update()

        self.show_snackbar(f"已切换到{e.control.selected_index}统计", "info")

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
