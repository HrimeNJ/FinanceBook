"""
FinanceBook Desktop Application Entry Point

Run this file to start the FinanceBook application.
"""

import flet as ft

from app import FinanceBookApp


def main(page: ft.Page):
    """应用主入口"""
    app = FinanceBookApp()
    app.main(page)


if __name__ == "__main__":
    ft.app(target=main)
