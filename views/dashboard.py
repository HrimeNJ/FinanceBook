"""
Dashboard for ui
"""

from datetime import datetime

import flet as ft

from components.cards import create_stat_card
from components.sidebar import Sidebar


class DashboardView(ft.View):
    """仪表板视图"""

    def __init__(self, state, go):
        super().__init__(route="/dashboard")
        self.state = state
        self.go = go
        self.page = state.page
        self.controls = [self.create_dashboard_layout()]

    def create_dashboard_layout(self):
        """创建仪表板布局"""
        # 获取真实统计数据
        user_stats = self.get_user_dashboard_stats()

        # 侧边栏
        sidebar = Sidebar(
            self.page, self.state.current_user, self.handle_logout, self.go
        ).create_sidebar()

        # 主内容
        main_content = ft.Container(
            content=ft.Column(
                [
                    # 页面标题 - 固定在顶部
                    self.create_page_header(
                        "仪表板", datetime.now().strftime("%Y年%m月%d日")
                    ),
                    # 可滚动的内容区域
                    ft.Container(
                        content=ft.Column(
                            [
                                # 统计卡片 - 显示真实数据
                                ft.Container(
                                    content=ft.ResponsiveRow(
                                        [
                                            ft.Container(
                                                content=create_stat_card(
                                                    "总收入",
                                                    f"¥{user_stats['total_income']:.2f}",
                                                    f"{user_stats['income_change']:+.1f}%",
                                                    ft.Colors.GREEN_400,
                                                    ft.Icons.TRENDING_UP,
                                                ),
                                                col={"sm": 12, "md": 4},
                                            ),
                                            ft.Container(
                                                content=create_stat_card(
                                                    "总支出",
                                                    f"¥{user_stats['total_expenses']:.2f}",
                                                    f"{user_stats['expense_change']:+.1f}%",
                                                    ft.Colors.RED_400,
                                                    ft.Icons.TRENDING_DOWN,
                                                ),
                                                col={"sm": 12, "md": 4},
                                            ),
                                            ft.Container(
                                                content=create_stat_card(
                                                    "当前余额",
                                                    f"¥{user_stats['current_balance']:.2f}",
                                                    f"{user_stats['balance_change']:+.1f}%",
                                                    ft.Colors.BLUE_400,
                                                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                                                ),
                                                col={"sm": 12, "md": 4},
                                            ),
                                        ],
                                        spacing=16,
                                    ),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                ),
                                # 快速操作
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "快速操作",
                                                size=16,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            ft.Container(height=12),
                                            ft.Row(
                                                [
                                                    ft.Container(
                                                        content=ft.ElevatedButton(
                                                            text="添加收入",
                                                            icon=ft.Icons.ADD_CIRCLE,
                                                            style=ft.ButtonStyle(
                                                                bgcolor=ft.Colors.GREEN_600,
                                                                color=ft.Colors.WHITE,
                                                                shape=ft.RoundedRectangleBorder(
                                                                    radius=8
                                                                ),
                                                            ),
                                                            on_click=lambda e: self.go(
                                                                "/add_record"
                                                            ),
                                                        ),
                                                        col={"sm": 12, "md": 4},
                                                    ),
                                                    ft.Container(
                                                        content=ft.ElevatedButton(
                                                            text="添加支出",
                                                            icon=ft.Icons.REMOVE_CIRCLE,
                                                            style=ft.ButtonStyle(
                                                                bgcolor=ft.Colors.RED_600,
                                                                color=ft.Colors.WHITE,
                                                                shape=ft.RoundedRectangleBorder(
                                                                    radius=8
                                                                ),
                                                            ),
                                                            on_click=lambda e: self.go(
                                                                "/add_record"
                                                            ),
                                                        ),
                                                        col={"sm": 12, "md": 4},
                                                    ),
                                                    ft.Container(
                                                        content=ft.ElevatedButton(
                                                            text="查看报告",
                                                            icon=ft.Icons.ANALYTICS,
                                                            style=ft.ButtonStyle(
                                                                bgcolor=ft.Colors.BLUE_600,
                                                                color=ft.Colors.WHITE,
                                                                shape=ft.RoundedRectangleBorder(
                                                                    radius=8
                                                                ),
                                                            ),
                                                            on_click=lambda e: self.go(
                                                                "/statistics"
                                                            ),
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
                                # 最近交易 - 显示真实数据
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text(
                                                        "最近交易",
                                                        size=20,
                                                        weight=ft.FontWeight.BOLD,
                                                        color=ft.Colors.GREY_800,
                                                    ),
                                                    ft.TextButton(
                                                        text="查看全部 →",
                                                        on_click=lambda e: self.go(
                                                            "/records"
                                                        ),
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            ),
                                            ft.Container(height=16),
                                            self.create_recent_transactions_list(),
                                        ]
                                    ),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.all(20),
                                    margin=ft.margin.symmetric(
                                        horizontal=20, vertical=10
                                    ),
                                    border=ft.border.all(1, ft.Colors.GREY_200),
                                    # 移除expand=True，让它根据内容自适应高度
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
            content=ft.Column(
                [
                    ft.Row(
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
                    ft.Container(height=8),
                    ft.Text(
                        f"欢迎回来，{self.state.current_user.username if self.state.current_user else '用户'}！",
                        size=16,
                        color=ft.Colors.GREY_700,
                    ),
                ],
                spacing=0,
            ),
            padding=ft.padding.symmetric(horizontal=30, vertical=30),
        )

    def get_user_dashboard_stats(self) -> dict:
        """获取用户仪表板统计数据"""
        if not self.state.current_user:
            return self.get_empty_stats()

        try:
            # 从数据库获取用户余额数据
            balance_data = self.state.db.get_user_balance(
                self.state.current_user.user_id
            )

            total_income = balance_data.get("income", 0)
            total_expenses = balance_data.get("expense", 0)
            current_balance = total_income - total_expenses

            # 计算变化率（简化版本，实际应该对比上期数据）
            # 这里使用模拟数据，实际应该从数据库获取上期数据进行对比
            income_change = self.calculate_change_percentage("income")
            expense_change = self.calculate_change_percentage("expense")
            balance_change = income_change - expense_change

            return {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "current_balance": current_balance,
                "income_change": income_change,
                "expense_change": expense_change,
                "balance_change": balance_change,
            }
        except Exception as e:
            print(f"获取统计数据失败: {e}")
            return self.get_empty_stats()

    def get_empty_stats(self) -> dict:
        """获取空统计数据"""
        return {
            "total_income": 0,
            "total_expenses": 0,
            "current_balance": 0,
            "income_change": 0,
            "expense_change": 0,
            "balance_change": 0,
        }

    def calculate_change_percentage(self, record_type: str) -> float:
        """计算变化百分比（简化版）"""
        try:
            # 获取当前月和上月的数据
            from datetime import datetime, timedelta

            now = datetime.now()
            current_month_start = now.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)

            # 获取当前月数据
            current_records = self.state.db.query(
                """SELECT SUM(amount) as total FROM records 
                   WHERE user_id = ? AND record_type = ? AND date >= ?""",
                (
                    self.state.current_user.user_id,
                    record_type,
                    current_month_start.strftime("%Y-%m-%d"),
                ),
            )
            current_total = (
                current_records[0]["total"]
                if current_records and current_records[0]["total"]
                else 0
            )

            # 获取上月数据
            last_records = self.state.db.query(
                """SELECT SUM(amount) as total FROM records 
                   WHERE user_id = ? AND record_type = ? AND date >= ? AND date < ?""",
                (
                    self.state.current_user.user_id,
                    record_type,
                    last_month_start.strftime("%Y-%m-%d"),
                    current_month_start.strftime("%Y-%m-%d"),
                ),
            )
            last_total = (
                last_records[0]["total"]
                if last_records and last_records[0]["total"]
                else 0
            )

            # 计算变化百分比
            if last_total == 0:
                return 100.0 if current_total > 0 else 0.0

            change = ((current_total - last_total) / last_total) * 100
            return round(change, 1)
        except Exception as e:
            print(f"计算变化百分比失败: {e}")
            return 0.0

    def create_recent_transactions_list(self):
        """创建最近交易列表"""
        try:
            if not self.state.current_user:
                return ft.Container(
                    content=ft.Text("请先登录", text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    height=200,
                )

            # 获取最近5条记录
            records = self.state.db.get_records(
                self.state.current_user.user_id, limit=5, order_by="date DESC"
            )

            if not records:
                return ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.RECEIPT_LONG, size=48, color=ft.Colors.GREY_400
                            ),
                            ft.Text(
                                "暂无交易记录",
                                size=16,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "点击上方按钮添加您的第一笔记录",
                                size=12,
                                color=ft.Colors.GREY_500,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    alignment=ft.alignment.center,
                    height=200,
                )

            # 创建交易列表
            transaction_items = []
            for record in records:
                # 获取分类信息
                category = self.state.db.get_category(record.category_id)
                category_name = category.name if category else "未知分类"

                # 创建交易项
                transaction_item = ft.Container(
                    content=ft.Row(
                        [
                            # 图标
                            ft.Container(
                                content=ft.Icon(
                                    (
                                        ft.Icons.ARROW_UPWARD
                                        if record.record_type == "income"
                                        else ft.Icons.ARROW_DOWNWARD
                                    ),
                                    color=ft.Colors.WHITE,
                                    size=20,
                                ),
                                bgcolor=(
                                    ft.Colors.GREEN
                                    if record.record_type == "income"
                                    else ft.Colors.RED
                                ),
                                border_radius=20,
                                width=40,
                                height=40,
                                alignment=ft.alignment.center,
                            ),
                            # 交易信息
                            ft.Column(
                                [
                                    ft.Text(
                                        record.note or category_name,
                                        size=14,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.GREY_900,
                                    ),
                                    ft.Text(
                                        f"{category_name} • {record.date.strftime('%m月%d日')}",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            # 金额
                            ft.Text(
                                f"{'+'if record.record_type == 'income' else '-'}¥{record.amount:.2f}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=(
                                    ft.Colors.GREEN
                                    if record.record_type == "income"
                                    else ft.Colors.RED
                                ),
                            ),
                        ],
                        spacing=12,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.symmetric(vertical=8, horizontal=4),
                    border_radius=8,
                    ink=True,
                )
                transaction_items.append(transaction_item)

            return ft.Column(
                controls=transaction_items,
                spacing=4,
                scroll=ft.ScrollMode.AUTO,
            )

        except Exception as e:
            print(f"创建最近交易列表失败: {e}")
            return ft.Container(
                content=ft.Text("加载交易记录失败", text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center,
                height=200,
            )

    def handle_logout(self, e):
        """处理登出"""

        def confirm_logout(confirm_e):
            dialog.open = False
            self.page.update()

            if confirm_e.control.text == "确认":
                self.state.clear_user_data()
                self.go("/welcome")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("确认登出"),
            content=ft.Text("您确定要登出吗？"),
            actions=[
                ft.TextButton("取消", on_click=confirm_logout),
                ft.TextButton("确认", on_click=confirm_logout),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

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
