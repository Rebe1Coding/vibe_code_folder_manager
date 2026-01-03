import flet as ft
from parser import StructureParser, StructureCreator


class ModernColors:
    """Современная цветовая схема"""
    PRIMARY = "#6366f1"  # Indigo
    PRIMARY_DARK = "#4f46e5"
    SECONDARY = "#8b5cf6"  # Purple
    SUCCESS = "#10b981"  # Green
    ERROR = "#ef4444"  # Red
    WARNING = "#f59e0b"  # Amber
    BG_DARK = "#1e1b4b"  # Dark indigo
    BG_LIGHT = "#f8fafc"
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"


class ProjectStructureApp:
    """Главное приложение с современным дизайном"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()
        self.parser = StructureParser()
        self.selected_path = None
        self._build_ui()
    
    def _setup_page(self):
        """Настройка страницы"""
        self.page.title = "Project Structure Generator"
        self.page.window.width = 1000
        self.page.window.height = 750
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ModernColors.BG_LIGHT
    
    def _build_ui(self):
        """Создает пользовательский интерфейс"""
        
        # Заголовок приложения
        header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.FOLDER_SPECIAL, color="white", size=40),
                ft.Text(
                    "Project Structure Generator",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ModernColors.PRIMARY,
            padding=25,
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20)
        )
        
        # Поле для выбора пути
        self.path_field = ft.TextField(
            label="📂 Путь для создания структуры",
            read_only=True,
            hint_text="Выберите папку где будет создан проект...",
            border_color=ModernColors.PRIMARY,
            focused_border_color=ModernColors.PRIMARY_DARK,
            text_size=14,
            height=60
        )
        
        # Кнопка выбора папки
        self.pick_folder_btn = ft.ElevatedButton(
            "Выбрать папку",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=self._pick_folder,
            style=ft.ButtonStyle(
                bgcolor=ModernColors.PRIMARY,
                color="white",
                padding=15,
            ),
            height=55,
            width=180
        )
        
        # Секция выбора пути
        path_section = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.path_field,
                    self.pick_folder_btn
                ], spacing=10),
            ]),
            padding=20,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, "black"),
            )
        )
        
        # Поле для ввода структуры
        self.structure_input = ft.TextField(
            label="📝 Структура проекта (Markdown формат)",
            multiline=True,
            min_lines=12,
            max_lines=12,
            hint_text="project-name/\n├── README.md\n├── src/\n│   └── main.py\n...",
            border_color=ModernColors.SECONDARY,
            focused_border_color=ModernColors.PRIMARY,
            text_style=ft.TextStyle(font_family="Courier New", size=13)
        )
        
        # Кнопка создания структуры
        self.create_btn = ft.ElevatedButton(
            "Создать структуру проекта",
            icon=ft.Icons.ROCKET_LAUNCH,
            on_click=self._create_structure,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ModernColors.SUCCESS,
                    ft.ControlState.DISABLED: ModernColors.TEXT_SECONDARY,
                },
                color="white",
                padding=18,
            ),
            height=55,
            width=250
        )
        
        # Секция ввода структуры
        input_section = ft.Container(
            content=ft.Column([
                self.structure_input,
                ft.Row([
                    self.create_btn,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            ], spacing=15),
            padding=20,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, "black"),
            )
        )
        
        # Поле для логов
        self.log_field = ft.TextField(
            label="📋 Лог создания",
            multiline=True,
            read_only=True,
            min_lines=10,
            max_lines=10,
            border_color=ModernColors.TEXT_SECONDARY,
            text_style=ft.TextStyle(font_family="Courier New", size=12),
            value="Готов к работе... 🚀\n"
        )
        
        # Секция логов
        log_section = ft.Container(
            content=self.log_field,
            padding=20,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, "black"),
            )
        )
        
        # Диалог выбора папки
        self.folder_picker = ft.FilePicker(on_result=self._folder_picked)
        self.page.overlay.append(self.folder_picker)
        
        # Основной контейнер
        main_content = ft.Container(
            content=ft.Column([
                header,
                ft.Container(
                    content=ft.Column([
                        path_section,
                        input_section,
                        log_section,
                    ], spacing=20),
                    padding=20,
                )
            ], spacing=0, scroll=ft.ScrollMode.AUTO),
            expand=True
        )
        
        self.page.add(main_content)
    
    def _pick_folder(self, e):
        """Обработчик выбора папки"""
        self.folder_picker.get_directory_path(dialog_title="Выберите папку для проекта")
    
    def _folder_picked(self, e: ft.FilePickerResultEvent):
        """Обработчик результата выбора папки"""
        if e.path:
            self.selected_path = e.path
            self.path_field.value = e.path
            self.create_btn.disabled = False
            self._log(f"✅ Выбран путь: {e.path}\n")
            self.page.update()
    
    def _log(self, message: str):
        """Добавляет сообщение в лог"""
        current = self.log_field.value or ""
        self.log_field.value = current + message + "\n"
        self.page.update()
    
    def _create_structure(self, e):
        """Создает файловую структуру"""
        if not self.selected_path:
            self._show_error("❌ Ошибка", "Пожалуйста, выберите папку!")
            return
        
        if not self.structure_input.value:
            self._show_error("❌ Ошибка", "Пожалуйста, введите структуру проекта!")
            return
        
        # Очищаем лог
        self.log_field.value = ""
        self._log("=" * 70)
        self._log("🚀 Начинаем создание структуры проекта...")
        self._log("=" * 70 + "\n")
        
        try:
            # Парсим структуру
            self._log("📖 [1/3] Парсинг структуры...")
            parsed = self.parser.parse(self.structure_input.value)
            self._log(f"   ✓ Элементов для создания: {len(parsed)-1}\n")
            root_folder, paths = self.parser.build_paths(parsed)
            
            if not root_folder:
                self._show_error("❌ Ошибка", "Не удалось определить корневую папку проекта!")
                return
            
            self._log(f"   ✓ Корневая папка: {root_folder}/")
            self._log(f"   ✓ Найдено элементов: {len(paths)}\n")
            
            # Создаем структуру
            self._log("🔨 [2/3] Создание файлов и директорий...\n")
            creator = StructureCreator(self.selected_path, self._log)
            dirs, files, errors = creator.create(root_folder, paths)
            
            # Итоги
            self._log("\n" + "=" * 70)
            self._log("✨ [3/3] Завершено!")
            self._log("=" * 70)
            self._log(f"📊 Статистика:")
            self._log(f"   📁 Создано директорий: {dirs}")
            self._log(f"   📄 Создано файлов: {files}")
            
            if errors:
                self._log(f"   ❌ Ошибок: {len(errors)}")
                self._show_warning(
                    "⚠️ Структура создана с ошибками",
                    f"Путь: {self.selected_path}/{root_folder}/\n"
                    f"Директорий: {dirs}\n"
                    f"Файлов: {files}\n"
                    f"Ошибок: {len(errors)}\n\n"
                    f"Проверьте лог для деталей."
                )
            else:
                self._log(f"   ✅ Ошибок: 0")
                self._show_success(
                    "🎉 Успешно!",
                    f"Структура проекта успешно создана!\n\n"
                    f"📂 Путь: {self.selected_path}/{root_folder}/\n"
                    f"📁 Директорий: {dirs}\n"
                    f"📄 Файлов: {files}"
                )
                
        except Exception as ex:
            self._log(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {str(ex)}")
            self._show_error("❌ Критическая ошибка", f"Произошла ошибка:\n{str(ex)}")
    
    def _show_error(self, title: str, message: str):
        """Показывает диалог ошибки"""
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.ERROR, color=ModernColors.ERROR, size=30),
                ft.Text(title, color=ModernColors.ERROR, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Text(message),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self._close_dialog(dialog),
                    style=ft.ButtonStyle(color=ModernColors.ERROR)
                )
            ]
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _show_success(self, title: str, message: str):
        """Показывает диалог успеха"""
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ModernColors.SUCCESS, size=30),
                ft.Text(title, color=ModernColors.SUCCESS, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Text(message),
            actions=[
                ft.TextButton(
                    "Отлично!",
                    on_click=lambda e: self._close_dialog(dialog),
                    style=ft.ButtonStyle(color=ModernColors.SUCCESS)
                )
            ]
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _show_warning(self, title: str, message: str):
        """Показывает диалог предупреждения"""
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ModernColors.WARNING, size=30),
                ft.Text(title, color=ModernColors.WARNING, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Text(message),
            actions=[
                ft.TextButton(
                    "Понятно",
                    on_click=lambda e: self._close_dialog(dialog),
                    style=ft.ButtonStyle(color=ModernColors.WARNING)
                )
            ]
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _close_dialog(self, dialog):
        """Закрывает диалог"""
        dialog.open = False
        self.page.update()