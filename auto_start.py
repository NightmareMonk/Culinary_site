#!/usr/bin/env python3
"""
Автоматический запуск Django сервера
"""
import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def start_django_server():
    """Запуск Django сервера"""
    try:
        # Получаем директорию проекта
        project_dir = Path(__file__).parent
        os.chdir(project_dir)
        
        print("🚀 Запуск кулинарного сайта...")
        print("📁 Директория проекта:", project_dir)
        print("🌐 Сайт будет доступен по адресу: http://127.0.0.1:8000/")
        print("⏹️  Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        # Запускаем Django сервер
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске сервера: {e}")
        input("Нажмите Enter для выхода...")

def check_dependencies():
    """Проверка зависимостей"""
    try:
        import django
        print(f"✅ Django {django.get_version()} установлен")
    except ImportError:
        print("❌ Django не установлен. Установите: pip install django")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow установлен")
    except ImportError:
        print("❌ Pillow не установлен. Установите: pip install Pillow")
        return False
    
    return True

def main():
    """Главная функция"""
    print("=" * 50)
    print("🍳 КУЛИНАРНЫЙ САЙТ - АВТОЗАПУСК")
    print("=" * 50)
    
    # Проверяем зависимости
    if not check_dependencies():
        input("Нажмите Enter для выхода...")
        return
    
    # Проверяем наличие manage.py
    if not Path("manage.py").exists():
        print("❌ Файл manage.py не найден!")
        print("Убедитесь, что вы находитесь в директории Django проекта")
        input("Нажмите Enter для выхода...")
        return
    
    # Запускаем сервер
    start_django_server()

if __name__ == "__main__":
    main()
