import os
import re
from pathlib import Path
from typing import List, Tuple, Optional


class StructureParser:
    """Парсер markdown структуры проекта"""
    
    def __init__(self):
        self.tree_symbols = ['├──', '└──', '│', '─', '├', '└', '|']
    
    def parse(self, text: str) -> List[Tuple[str, int]]:
        """
        Парсит markdown структуру и возвращает список (путь, уровень_вложенности)
        
        Args:
            text: Markdown строка со структурой проекта
            
        Returns:
            List[Tuple[str, int]]: Список кортежей (имя_файла_или_папки, уровень)
        """
        lines = text.split('\n')
        result = []
        
        for line in lines[1:]:
            line = re.sub(r'#.*$', '', line)
            line = line.split()
            indent_level = (len(line)-1)
            if len(line) != 0:
                if line[-1]!= '│' and line[-1] != '':
                    cleaned = line[-1]
                    result.append((cleaned, indent_level))
        
        return result
    
    def build_paths(self, parsed: List[Tuple[str, int]]) -> Tuple[Optional[str], List[Tuple[str, bool]]]:
        """
        Строит полные пути из распарсенной структуры
        
        Args:
            parsed: Список кортежей (имя, уровень)
            
        Returns:
            Tuple[Optional[str], List[Tuple[str, bool]]]: 
                (имя_корневой_папки, список_путей)
                где список_путей = [(полный_путь, является_директорией)]
        """
        if not parsed:
            return None, []
        
        # Первая строка - это корневая папка проекта
        root_name, root_level = parsed[0]
        root_name = root_name.rstrip('/')
        
        paths = []
        stack = []  # Стек для отслеживания текущего пути
        
        # Обрабатываем остальные элементы (начиная со второго)
        for name, level in parsed[2:]:
            # Корректируем стек под текущий уровень (относительно корня)
            adjusted_level = level - root_level
            while len(stack) > adjusted_level:
                stack.pop()
            
            # Определяем, является ли элемент директорией
            is_dir = name.endswith('/')
            clean_name = name.rstrip('/')
            
            # Строим полный путь (относительно корня проекта)
            if stack:
                full_path = os.path.join(*stack, clean_name)
            else:
                full_path = clean_name
            
            paths.append((full_path, is_dir))
            
            # Добавляем в стек, если это директория
            if is_dir:
                stack.append(clean_name)
        
        return root_name, paths

class StructureCreator:
    """Создатель файловой структуры"""
    
    def __init__(self, base_path: str, log_callback=None):
        """
        Args:
            base_path: Базовый путь для создания структуры
            log_callback: Функция для логирования (принимает строку)
        """
        self.base_path = Path(base_path)
        self.log = log_callback or print
    
    def create(self, root_folder: str, paths: List[Tuple[str, bool]]) -> Tuple[int, int, List[str]]:
        """
        Создает файловую структуру
        
        Args:
            root_folder: Имя корневой папки проекта
            paths: Список кортежей (путь, является_директорией)
            
        Returns:
            Tuple[int, int, List[str]]: (кол-во_директорий, кол-во_файлов, список_ошибок)
        """
        dirs_created = 0
        files_created = 0
        errors = []
        
        # Создаем корневую папку проекта
        project_root = self.base_path / root_folder
        try:
            project_root.mkdir(parents=True, exist_ok=True)
            self.log(f"📁 Создана корневая папка проекта: {root_folder}/")
            dirs_created += 1
        except Exception as e:
            error_msg = f"❌ Ошибка при создании корневой папки {root_folder}: {str(e)}"
            self.log(error_msg)
            errors.append(error_msg)
            return dirs_created, files_created, errors
        
        # Создаем остальную структуру внутри корневой папки
        for rel_path, is_dir in paths:
            full_path = project_root / rel_path
            
            try:
                if is_dir:
                    full_path.mkdir(parents=True, exist_ok=True)
                    self.log(f"📁 Создана директория: {rel_path}/")
                    dirs_created += 1
                else:
                    # Создаем родительские директории, если нужно
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    # Создаем файл (перезаписываем если существует)
                    full_path.touch()
                    self.log(f"📄 Создан файл: {rel_path}")
                    files_created += 1
                    
            except Exception as e:
                error_msg = f"❌ Ошибка при создании {rel_path}: {str(e)}"
                self.log(error_msg)
                errors.append(error_msg)
        
        return dirs_created, files_created, errors