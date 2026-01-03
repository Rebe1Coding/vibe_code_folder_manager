import flet as ft
from ui import ProjectStructureApp


def main(page: ft.Page):
    """Точка входа приложения"""
    ProjectStructureApp(page)


if __name__ == "__main__":
    ft.app(target=main)